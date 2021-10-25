import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SALTUI_SECRET_KEY', 'pby)@shnci#e-m!4na$3u@1&j055rv(#wa&8#13wb_!t&af!2_')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.postgres',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'mozilla_django_oidc',
    'packages.apps.PackagesConfig',
    'system_info.apps.SystemInfoConfig',
    'users.apps.UsersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mozilla_django_oidc.middleware.SessionRefresh',
]

ROOT_URLCONF = 'saltui.urls'

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

WSGI_APPLICATION = 'saltui.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'saltui',
        'USER': os.getenv('SALTUI_DB_USER', ''),
        'PASSWORD': os.getenv('SALTUI_DB_PASS', ''),
        'HOST': os.getenv('SALTUI_DB_HOST', ''),
        'PORT': '5432',
        'CONN_MAX_AGE': 120
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'mozilla_django_oidc.auth.OIDCAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = '/accounts/login/'
# LOGIN_REDIRECT_URL = '/'

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# application specific settings
# options: api or local
SALT_CLIENT = os.getenv('SALTUI_SALT_CLIENT', 'api')

SALT_API_HOST = os.getenv('SALTUI_SALT_API_HOST', 'https://localhost:8000')
SALT_API_USER = os.getenv('SALTUI_SALT_API_USER', 'salt')
SALT_API_PASS = os.getenv('SALTUI_SALT_API_PASS', 'testing123')
SALT_API_EAUTH = os.getenv('SALTUI_SALT_API_EAUTH', 'sharedsecret')

PURGE_OLD_RECORDS = os.getenv('SALTUI_PURGE_OLD_RECORDS', True)
PURGE_OLDER_THAN = os.getenv('SALTUI_PURGE_OLDER_THAN', 5) # 5 days

# Okta
OKTA_DOMAIN = os.environ.get("OKTA_DOMAIN")
OKTA_TOKEN = os.environ.get("OKTA_TOKEN")

# User information
USER_CRM_ID = None
USER_EMAIL = None

# Okta Admin
OKTA_ADMIN_DOMAIN = OKTA_DOMAIN
OIDC_RP_SIGN_ALGO = "RS256"
OIDC_OP_JWKS_ENDPOINT = f"{OKTA_ADMIN_DOMAIN}/oauth2/v1/keys"
OIDC_OP_AUTHORIZATION_ENDPOINT = f"{OKTA_ADMIN_DOMAIN}/oauth2/v1/authorize"
OIDC_OP_TOKEN_ENDPOINT = f"{OKTA_ADMIN_DOMAIN}/oauth2/v1/token"
OIDC_OP_USER_ENDPOINT = f"{OKTA_ADMIN_DOMAIN}/oauth2/v1/userinfo"
OIDC_RP_SCOPES = "openid profile email groups"
OIDC_RP_CLIENT_ID = os.environ.get("OKTA_ADMIN_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = os.environ.get("OKTA_ADMIN_CLIENT_SECRET")
OIDC_VERIFY_SSL = True
LOGIN_REDIRECT_URL = "localhost:8080/admin/"
OIDC_REDIRECT_URL = "localhost:8080/admin/oidc/callback/"
OIDC_AUTH_REQUEST_EXTRA_PARAMS = {"redirect_uri": OIDC_REDIRECT_URL}