import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'pby)@shnci#e-m!4na$3u@1&j055rv(#wa&8#13wb_!t&af!2_')

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
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASS', ''),
        'HOST': os.getenv('DB_HOST', ''),
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

OIDC_RP_SIGN_ALGO = os.getenv('OIDC_RP_SIGN_ALGO', 'HS256')
OIDC_OP_JWKS_ENDPOINT = os.getenv('OIDC_OP_JWKS_ENDPOINT')
OIDC_OP_AUTHORIZATION_ENDPOINT = os.getenv('OIDC_OP_AUTHORIZATION_ENDPOINT')
OIDC_OP_TOKEN_ENDPOINT = os.getenv('OIDC_OP_TOKEN_ENDPOINT')
OIDC_OP_USER_ENDPOINT = os.getenv('OIDC_OP_USER_ENDPOINT')
OIDC_RP_SCOPES = os.getenv('OIDC_RP_SCOPE', 'openid email')
OIDC_RP_CLIENT_ID = os.getenv('OIDC_RP_CLIENT_ID', '')
OIDC_RP_CLIENT_SECRET = os.getenv('OIDC_RP_CLIENT_SECRET', '')
LOGIN_REDIRECT_URL = os.getenv('APP_BASE_DOMAIN', '/')
# OIDC_REDIRECT_URL = f"{BASE_URL}/admin/oidc/callback/"
# OIDC_AUTH_REQUEST_EXTRA_PARAMS = {"redirect_uri": OIDC_REDIRECT_URL}
# LOGOUT_REDIRECT_URL = "<URL path to redirect to after logout>"

# OKTA_AUTH = {
#     'ORG_URL': 'https://' + os.getenv('OKTA_DOMAIN', '') + '/',
#     'ISSUER': 'https://' + os.getenv('OKTA_DOMAIN', '') + '/oauth2/default',
#     'CLIENT_ID': os.getenv('OKTA_CLIENT_ID', ''),
#     'CLIENT_SECRET': os.getenv('OKTA_CLIENT_SECRET', ''),
#     'SCOPES': 'openid profile email groups offline_access', # this is the default and can be omitted
#     'REDIRECT_URI': os.getenv('APP_BASE_DOMAIN', 'http://localhost:8080') + '/accounts/oauth2/callback/',
#     'LOGIN_REDIRECT_URL': os.getenv('APP_BASE_DOMAIN', '/'),
#     'CACHE_PREFIX': 'okta', # default
#     'CACHE_ALIAS': 'default', # default
#     'PUBLIC_NAMED_URLS': (), # list or tuple of URL names that should be accessible without tokens
#     'PUBLIC_URLS': (), # list or tuple of URL regular expressions that should be accessible without tokens
#     'MANAGE_GROUPS': False, # if true the authentication backend will manage django groups for you; include groups in scopes if true
#     'STAFF_GROUP': 'admin', # members of this group will have the django is_staff user flags set
#     'SUPERUSER_GROUP': 'admin', # members of this group will have the django is_superuser user flags set.
# }

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
SALT_CLIENT = os.getenv('SALT_CLIENT', 'api')

SALT_API_HOST = os.getenv('SALT_API_HOST', 'https://localhost:8000')
SALT_API_USER = os.getenv('SALT_API_USER', 'salt')
SALT_API_PASS = os.getenv('SALT_API_PASS', 'testing123')
SALT_API_EAUTH = os.getenv('SALT_API_EAUTH', 'sharedsecret')

PURGE_OLD_RECORDS = os.getenv('PURGE_OLD_RECORDS', True)
PURGE_OLDER_THAN = os.getenv('PURGE_OLDER_THAN', 5) # 5 days