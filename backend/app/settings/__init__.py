import os

if(os.getenv('DJANGO_ENV')) == 'production':
    from .production import *
else:
    from .develoment import *
    print('code hrer')