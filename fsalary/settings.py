"""
Django settings for fsalary project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# BEGIN handle the unicode problem
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
# END handle the unicode problem

from private_settings import *
import elasticsearch
from requests_aws4auth import AWS4Auth

awsauth = AWS4Auth(AWSAccessKeyId, AWSSecretKey, AWS_ES_FSALARY_REGION , 'es')

########################################
# Haystack Settings BEGIN
########################################
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': AWS_ES_FSALARY_ENDPOINT,
        'TIMEOUT': 10 * 6, #1 min
        'INDEX_NAME': 'haystack',
        'INCLUDE_SPELLING': True,
        'KWARGS':{
            'port':443,
            'http_auth':awsauth,
            'use_ssl':True,
            'verify_certs':True,
            'connection_class':elasticsearch.RequestsHttpConnection,
        },
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack_rqueue.signals.RQueueSignalProcessor'


RQ_QUEUES = {
    'default': {
        'HOST': AWS_CACHE_HAYSTACKRQ_ENDPOINT,
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT':360,
    },
}

########################################
# Haystack Settings END
########################################




# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = FRANKSALARY_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost','0.0.0.0']

#registration-redux
ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window
REGISTRATION_AUTO_LOGIN = True # Automatically log the user in.


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'registration',
    'reviews',
    'elasticsearch',
    'django_nvd3',
    'djangobower',
    'bootstrap3',

    #django debug toolbar
    #'debug_toolbar',

    #queue up the search jobs with Redis Queue
    'haystack',
    'django_rq',
    'haystack_rqueue',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    #django debug toolbar
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'fsalary.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR+'/templates/',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fsalary.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': FRANKSALARY_DATABASE_NAME,
        'USER': FRANKSALARY_DATABASE_USER,
        'PASSWORD': FRANKSALARY_DATABASE_PWD,
        'HOST': FRANKSALARY_DATABASE_HOST,
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#STATIC_DIRS = (os.path.join(BASE_DIR, 'static'),)




# Django-bower
# ------------
STATICFILES_FINDERS = (
    'djangobower.finders.BowerFinder',
)

BOWER_PATH = '/usr/local/bin/bower'


# Specifie path to components root (you need to use absolute path)
BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'components')

BOWER_INSTALLED_APPS = (
    'd3#3.5.16',
    'nvd3#1.8.1',
)



