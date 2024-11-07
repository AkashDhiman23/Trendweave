"""
Django settings for Trendweave_users project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3mhdwi7l63$+u5j8h-jk2z3&zyk-rt1k7wj59wul4b3r&*5h25'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True



AUTHENTICATION_BACKENDS = [
    'Userpanel.auth_backends.CustomUserBackend',  
    'django.contrib.auth.backends.ModelBackend',  # Keep the default backend if needed
]


ALLOWED_HOSTS = []

# AUTHENTICATION_BACKENDS = (
#     'Userpanel.backends.EmailBackend', 
#     'django.contrib.auth.backends.ModelBackend',  # Keep the default as a fallback
# )


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'admin_panel',  # Make sure this is included
    'Userpanel',    # Ensure Userpanel is also included
    
]

MIDDLEWARE = [
    
 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
     'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',


    
]

ROOT_URLCONF = 'Trendweave_users.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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


WSGI_APPLICATION = 'Trendweave_users.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Trendweavedb',        
        'USER': 'postgres',         
        'PASSWORD': 'dhiman223', 
        'HOST': 'localhost',            
        'PORT': '5432',                 
    }
}
# settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'Userpanel/static',  
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.office365.com'  # For Office 365
EMAIL_PORT = 587  # Use 587 for TLS
EMAIL_USE_TLS = True  # Set to True for TLS
EMAIL_HOST_USER = 'trendweavenz@outlook.com'  
EMAIL_HOST_PASSWORD = 'trendweave@123'  
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

LOGIN_URL = '/login/'

STRIPE_TEST_PUBLIC_KEY = 'pk_test_51PJPlI098w1868DgStq59Ol9oGjPuVzf9Gi8w1aSa3UFFPU4gtKoum5KPA2DymTGWGHDh1p6Hb1JoIrVUb3CsBV700mRl7AgzB'
STRIPE_TEST_SECRET_KEY = 'sk_test_51PJPlI098w1868Dgc6pSzhp7ESO87GRpL89KmZVlHl6TdRLtaeRokRO5RkJPOmS7oCsCddTlPP3SGqjFAez52rs300lxnlV9Lg'


