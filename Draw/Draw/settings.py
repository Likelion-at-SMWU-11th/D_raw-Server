from pathlib import Path
import os, json
from datetime import timedelta
from telnetlib import AUTHENTICATION
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL =  '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ld1ko$)@5+fww$(+rhqo^4!q*!!3%!yx(l@dk=^*s_fc$nhda_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #site 설정
    'django.contrib.sites',

    # 생성한 app
    'main',
    'match',
    'account',

    # 설치한 라이브러리
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'dj_rest_auth',
    'dj_rest_auth.registration',

    'allauth',
    #'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao',
]

AUTH_USER_MODEL = 'account.User'


# secret key -> secrets.json
secret_file = os.path.join(BASE_DIR, 'secrets.json') #json 파일 위치를 명시
secrets = None
with open(secret_file) as f:
    secrets = json.loads(f.read())

SECRET_KEY = secrets['SECRET_KEY']

# 카카오 키들은 나중에 account.views 에서 쓰일 예정

# SOCIAL_OUTH_CONFIG = { # 오류 때문에 주석 처리
#     'KAKAO_REST_API_KEY':secrets['KAKAO_REST_API_KEY'],
#     'KAKAO_REDIRECT_URI':secrets['KAKAO_REDIRECT_URI'],
#     'KAKAO_SECRET_KEY': secrets['KAKAO_SECRET_KEY']
# }

kakao_login_uri = "https://kauth.kakao.com/oauth/authorize"
kakao_token_uri = "https://kauth.kakao.com/oauth/token"
kakao_profile_uri = "https://kapi.kakao.com/v2/user/me"

SITE_ID = 2 #django admin 사이트 접속 시 에러나는 것 방지

LOGIN_REDIRECT_URL ='/' #로그인 후 리다이렉트 될 경로
#ACCOUNT_LOGOUT_REDIRECT_URL = reverse_lazy('account:login')
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_AUTHENTICATION_METHOD = 'user_id'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FILED = None

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'Draw.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'Draw.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/


LANGUAGE_CODE = 'ko-kr' # 한국 시간으로 설정

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIAL_OUTH_CONFIG = {
    "KAKAO_REST_API_KEY": secrets['KAKAO_REST_API_KEY'],
    "KAKAO_REDIRECT_URI": secrets['KAKAO_REDIRECT_URI'],
    "KAKAO_SECRET_KEY": secrets['KAKAO_SECRET_KEY']
}
# Rest-framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',)
}

REST_USE_JWT = True


SOCIALACCOUNT_PROVIDERS = {
    'kakao': {
        'APP': {
            'client_id': 'd8fd6327b24b302b1d20f0690b10d3f4',
            'secret': 948052,
            'key': ''
        }
    },
}


REST_USE_JWT = True

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',  # User 모델 연결
}


CORS_ORIGIN_ALLOW_ALL = False

# 접근 가능한 url 을 따로 관리
CORS_ORIGIN_WHITELIST = ('http://127.0.0.1:8000', 'http://localhost:3000')

CORS_ALLOW_CREDENTIALS = True


AUTHENTICATION_BACKENDS = [
    # ... 기존 설정 ...
    'allauth.account.auth_backends.AuthenticationBackend',# settings.py
]
