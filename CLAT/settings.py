"""
Django settings for CLAT project.

Generated by 'django-admin startproject' using Django 1.9.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.abspath(__file__)
DIR_NAME = os.path.dirname(os.path.dirname(file_path))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'en$9nlc_xe9xsl3%h_z8fek88sc+%7g9oyvkeyjavau#h$p+qb'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True

#ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'rest_framework',
    'user_login',
    'teacher',
    'course_mang',
    'student',
    'course_test_handling',
    'assesment_engine',
    'tracker',
    'rating_managment',
    'payment',
    'django_extensions',
    'kronos',
    #'payu',
    # 'resumable',
    'admin_resumable',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter'
]

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'CLAT.user_middelware.TimeToVideo',
    'CLAT.user_middelware.SetLastVisitMiddleware'
]


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of 'allauth'
    'django.contrib.auth.backends.ModelBackend',

    # 'allauth' specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend'
]

ROOT_URLCONF = 'CLAT.urls'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/home/'

# DJANGO_COLORS="error=yellow/blue,blink;notice=magenta"
# Setting for logger
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/clat_logs/mylog.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },  
        'request_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/clat_logs/django_request.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },

    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
# end of logger file setting 



# File upload setting
FILE_UPLOAD_MAX_MEMORY_SIZE = 786432000

# Third party authentication settings
#SITE_ID = 7
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'

#SOCIALACCOUNT_ADAPTER = 'EDX.CLAT.allauth_adapter.SocialAccountAdapter'


# CELERY SETTINGS
BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


# Session related settings
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

SESSION_COOKIE_AGE = 24*60*60 

TEMPLATE_DIRS = (os.path.join(SETTINGS_PATH, 'templates')
    ,os.path.join(SETTINGS_PATH+'/user_login/', 'templates')
    )

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
            ],
        },
    },
]

WSGI_APPLICATION = 'CLAT.wsgi.application'

# Cache configuration
CACHES = {
"default": {
"BACKEND": "django_redis.cache.RedisCache",
"LOCATION": "redis://127.0.0.1:6379/1",
"OPTIONS": {
"CLIENT_CLASS": "django_redis.client.DefaultClient",
    }
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

# Payment details
PAYU_MODE = "TEST"

PAYU_INFO = {
            # test
            'merchant_key': "gtKFFx",
            'merchant_salt': "eCwWELxi",
            'payment_url': 'https://test.payu.in/_payment',
            
            # live
            # 'merchant_key': "XOty3D",
            # 'merchant_salt': "K0OPsACO",
            # 'payment_url': 'https://secure.payu.in/_payment',      
            
	    # for production environment use 'https://secure.payu.in/_payment'	    	
}
# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = '/var/www/server_static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static/"),
)

MEDIA_ROOT = '/lms/media/'
MEDIA_URL = '/media/'

SITE_NAME = ''
try:
    from local_settings import *
    '''USE WHEN GENRATE TEST LINK TO REDIRECT AFTER TAKE TEST'''
except ImportError as e:
    pass

try:
    from server_settings import *
    '''USE TO GENERATE TEST LINK TO REDIRECT AFTER TAKE TEST'''
   
except ImportError as e:
    pass
