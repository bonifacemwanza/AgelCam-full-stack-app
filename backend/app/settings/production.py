from .base import *

DEBUG = False

ALLOWED_HOSTS = ['your-production-domain.com']

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    'https://your-frontend-domain.com',
]

DATABASES['default'].update({
    'HOST': os.getenv('DB_HOST', 'localhost'),
})