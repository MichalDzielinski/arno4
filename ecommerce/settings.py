from pathlib import Path
import os
from dotenv import load_dotenv

#region BASE SETTINGS & DEPLOYMENT
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG')
ALLOWED_HOSTS = ['*']

ROOT_URLCONF = "ecommerce.urls"

WSGI_APPLICATION = "ecommerce.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"
#endregion

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    #third party apps
    'crispy_forms',
    'crispy_bootstrap5',
    'storages',
    'mathfilters',
    #xustom apps
    "store",
    "payment",
    "cart",
    "account",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR, 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'store.context-processors.categories',
                'cart.context-processors.cart',
            ],
        },
    },
]

#region BOOTSTRAP SETTINGS
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK='bootstrap5'
#endregion

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

#region  LANGUAGE & TIME
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
#endregion

#region STATIC & MEDIA FILES
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'static/media'

#endregion

#region S# bucket settings
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY') 
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

# Django 4.2 > Storage configuration for S3

STORAGES = {
    
    # Media file (image) management

    "default": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
    },
    
    # CSS and JS file management

    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
        
    },
    
}


AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_FILE_OVERWRITE = False


#endregion




AUTH_USER_MODEL = 'account.CustomUser'

#region EMAIL SETTINGS

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'backupaddress7779311@gmail.com'
EMAIL_HOST_PASSWORD = 'pqvhttrtdgmyftie'
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL = 'Blog project <backupaddress7779311@gmail.com>'

#endregion