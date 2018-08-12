
import os 

from .base import *

# # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wsj-p0q$%*n)$hds&59!$1bg@p^9wyx$&9^nm*gba$3aurz=q1'

DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0']


INSTALLED_APPS += [
    'debug_toolbar',
]

# Application definition


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'socialteams',
        'USER': 'stuartmcintosh',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}
