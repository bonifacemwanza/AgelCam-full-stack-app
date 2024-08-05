from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import logging


import requests
logger = logging.getLogger(__name__)

class LoginView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)
        response = requests.get('https://api.angelcam.com/v1/me', headers={'Authorization': f'Bearer {token}'})
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response(response.json(), status=response.status_code)

class CameraListView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization')
        response = requests.get('https://api.angelcam.com/v1/cameras', headers={'Authorization': token})
        return Response(response.json(), status=response.status_code)

class CameraDetailView(APIView):
    def get(self, request, camera_id):
        token = request.headers.get('Authorization')
        live_response = requests.get(f'https://api.angelcam.com/v1/cameras/{camera_id}/live', headers={'Authorization': token})
        recordings_response = requests.get(f'https://api.angelcam.com/v1/cameras/{camera_id}/recordings', headers={'Authorization': token})
        return Response({
            "live": live_response.json(),
            "recordings": recordings_response.json()
        }, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class OAuth2LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            if not username or not password:
                return JsonResponse({'error': 'username and password required'}, status=400)

            print(settings.OAUTH2_CLIENT_ID)
            token_response = requests.post(settings.OAUTH2_TOKEN_URL, data={
                'grant_type': 'password',
                'client_id': settings.OAUTH2_CLIENT_ID,
                'username': username,
                'password': password,
                'scope': 'user_access',
            })

            # Log the status code and response text for debugging
            logger.debug(f"Token response status: {token_response.status_code}")
            logger.debug(f"Token response text: {token_response.text}")

            token_response.raise_for_status()
            token_data = token_response.json()

            if 'error' in token_data:
                return JsonResponse({'error': token_data['error']}, status=400)

            access_token = token_data['access_token']
            user_info_response = requests.get(settings.OAUTH2_USER_INFO_URL, headers={
                'Authorization': f'Bearer {access_token}'
            })
            user_info_response.raise_for_status()

            user_info = user_info_response.json()
            return JsonResponse({'access_token': access_token, 'user_info': user_info})

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTPError: {e}")
            return JsonResponse({'error': 'Failed to authenticate with Angelcam'}, status=e.response.status_code)
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {e}")
            return JsonResponse({'error': 'Failed to authenticate with Angelcam'}, status=500)
        except Exception as e:
            logger.error(f"Exception: {e}")
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
class OAuth2CallbackView(View):
    def get(self, request):
        code = request.GET.get('code')
        if not code:
            return JsonResponse({'error': 'Authorization code not provided'}, status=400)
        
        token_response = requests.post(settings.OAUTH2_TOKEN_URL, data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.OAUTH2_REDIRECT_URI,
            'client_id': settings.OAUTH2_CLIENT_ID,
            'client_secret': settings.OAUTH2_CLIENT_SECRET,
        })
        
        token_data = token_response.json()
        if 'error' in token_data:
            return JsonResponse({'error': token_data['error']}, status=400)
        
        access_token = token_data['access_token']
        user_info_response = requests.get(settings.OAUTH2_USER_INFO_URL, headers={
            'Authorization': f'Bearer {access_token}'
        })
        
        user_info = user_info_response.json()
        return JsonResponse(user_info)