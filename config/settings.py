from pathlib import Path
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-k_xtn(!%0g6yuvtx(%%j@inr^+ajb%l9pkhc0anok$&vs+=qxb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',  # Django admin paneli
    'django.contrib.auth',  # Foydalanuvchilarni boshqarish uchun autentifikatsiya
    'django.contrib.contenttypes',  # Kontent turlarini boshqarish
    'django.contrib.sessions',  # Sessiyalarni boshqarish
    'django.contrib.messages',  # Xabarlar tizimi
    'django.contrib.staticfiles',  # Statik fayllar (CSS, JavaScript, tasvirlar)
    'rest_framework',  # Django REST Framework (DRF) ni qo'shish
    'rest_framework_simplejwt',  # JWT autentifikatsiya kutubxonasi
    'drf_spectacular',
    
    'social_app',  # Yangi app yaratamiz, ijtimoiy tarmoq logikasini shu yerda yozamiz
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Foydalanuvchilarni faqat autentifikatsiya qilingan holda kirish imkonini beradi
    ],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Ijtimoiy tarmoq',  # Ma'lumotlar bazasi nomi
        'USER': 'postgres',  # PostgreSQL foydalanuvchi ismi
        'PASSWORD': 'zohidjon2008',  # PostgreSQL foydalanuvchi paroli
        'HOST': 'localhost',  # Agar lokalda ishlatilsa, 'localhost' bo'ladi
        'PORT': '5432',  # PostgreSQL porti (standarti 5432)
    }
}



SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Access tokenning amal qilish muddati (1 soat)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # Refresh tokenning amal qilish muddati (1 kun)
    'ROTATE_REFRESH_TOKENS': True,  # Har refresh qilishda yangi refresh token olish imkoniyati
    'BLACKLIST_AFTER_ROTATION': True,  # Eski refresh tokenni qora ro'yxatga qo'shish
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
