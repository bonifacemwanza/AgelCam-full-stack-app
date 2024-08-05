from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

CORS_ALLOW_ALL_ORIGINS = True

INSTALLED_APPS += [
    'django_extensions',
]
print("Loaded development settings")  # Debug statement
