import os
from pathlib import Path
import pymysql

# Fix for MySQL version check error
pymysql.version_info = (2, 2, 1, "final", 0)
pymysql.install_as_MySQLdb()

# BASE_DIR points to: D:\kmeans practice\kmeans-master
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-f5+a_5!h*zqo70*yv1o)skqi9zlaqgbu#&u6398g-&6l84kuki'

DEBUG = True  # Static files serve automatically when True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # Essential for serving CSS/JS
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'app' / 'templates'], 
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

WSGI_APPLICATION = 'project.wsgi.application'

# Database: Changed 'localhost' to '127.0.0.1' to fix the slow loading bug
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ANTARANGA',
        'USER': 'root',
        'PASSWORD': 'Abhinab@1234',
        'HOST': '127.0.0.1', 
        'PORT': '3306',
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Corrected STATICFILES_DIRS to match your project root 'static' folder
# This removes the W004 warning by pointing to the correct existing path
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Path where collectstatic will gather files for production
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'