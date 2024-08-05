from django.urls import path
from .views import LoginView, CameraListView, CameraDetailView, OAuth2CallbackView, OAuth2LoginView

app_name = 'api'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('cameras/', CameraListView.as_view(), name='camera_list'),
    path('cameras/<int:camera_id>/', CameraDetailView.as_view(), name='camera_detail'),
    path('oauth2/login/', OAuth2LoginView.as_view(), name='oauth2_login'),
    path('oauth2/callback/', OAuth2CallbackView.as_view(), name='oauth2_callback'),
]