"""
Django settings for fastparcel project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f88mj#!)pv2_jx8d^58+roz4rv2fuhx!@n7%7#lo$6fgy@(h&v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*',]
SECURE_SSL_REDIRECT=False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'bootstrap4',
    'social_django',
    'core.apps.CoreConfig',
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.ProfileMiddleware',
]

ROOT_URLCONF = 'fastparcel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'fastparcel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

LOGIN_URL = '/sign-in/'
LOGIN_REDIRECT_URL = '/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_FACEBOOK_KEY = "YOUR_FACEBOOK_CLIENT_KEY"
SOCIAL_AUTH_FACEBOOK_SECRET = "YOUR_FACEBOOK_SECRET_KEY"
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email'
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'tyraineytech@gmail.com'
EMAIL_HOST_PASSWORD = 'opbtdmygboipgaer'
DEFAULT_FROM_EMAIL = 'Fast Parcel <no-reply@fastparcel.localhost>' 
ACCOUNT_EMAIL_VERIFICATION = 'none'

FIREBASE_ADMIN_CREDENTIAL = os.path.join(BASE_DIR,"fastparcel-1c719-firebase-adminsdk-drpt3-5f3aba66ac.json")

STRIPE_API_PUBLIC_KEY = "pk_test_51MUlhfBtiQxYzJ3O8kUqgiIiXr2suu56rZUF1pjTzWPeEADWruq5Jf80wbFlbBtAU45no3hXLy6ODExte7rqmqe200IpeLD7EP"
STRIPE_API_SECRET_KEY = "sk_test_51MUlhfBtiQxYzJ3OsK6lu0vGJKkOBNegdDmT4bqZhmnoZl11RLFZu8JFakKv9UTpqc2KBWBpnAyOgmFKxh3dIxmj00nU8hBkKM"

GOOGLE_MAP_API_KEY = "AIzaSyBERO5oiERPINlBa8uA7hAnTK2pV_bS2go"

PAYPAL_MODE = "sandbox"
PAYPAL_CLIENT_ID = "AST3b8FkMxJBbggL2n9Guh1CljnhXkf9JNF-o8MlqBL7nDQW7zd0q2Dqm4xp0lwA7vTVwu6qSwvbbEgu"
PAYPAL_CLIENT_SECRET = "EPT-wklTzxuFMddgyzDxXIuQnJhWuHMMsjPprEM2QFdrZ3GLA0ZHxwUfBOj25-byjT0z8G_dGFoFiJSE"

NOTIFICATION_URL = "https://fastparcel.herokuapp.com/"

ASGI_APPLICATION = "fastparcel.asgi.application"


# Channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": ['redis://:p9029785bcd5c3b047aea28b392ef94ff559802b2b15a2a7c0a0d5df1055334ab@ec2-107-23-211-55.compute-1.amazonaws.com:31790'],
        },
    },
}

#Activate Django Heroku
import django_on_heroku
django_on_heroku.settings(locals())