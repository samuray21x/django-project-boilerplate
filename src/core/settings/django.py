import os
import environ

root = environ.Path(__file__) - 4
public_root = root.path('public/')
env = environ.Env()
environ.Env.read_env(root('.env'))

# Main Django settings
DEBUG = env.bool('DJANGO_DEBUG', False)
SECRET_KEY = env.str('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = env.str('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
INTERNAL_IPS = env.str('INTERNAL_IPS', 'localhost,127.0.0.1').split(',')

WSGI_APPLICATION = 'core.wsgi.application'
ROOT_URLCONF = 'core.urls'

# static & media files settings
SITE_ROOT = root()
STATIC_ROOT = public_root(env.str('STATIC_DIR', 'static'))
STATIC_URL = env.str('STATIC_URL_BASE', '/static/')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = public_root(env.str('MEDIA_DIR', 'media'))
MEDIA_URL = env.str('MEDIA_URL_BASE', '/media/')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'whitenoise',
    # 'debug_toolbar',

    # project apps
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',
    'core.middleware.MainExceptionMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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

# Databases
DATABASES = {
    'default': {
        'ENGINE': env.str('DB_ENGINE_DRIVER', 'django.db.backends.postgresql'),
        'NAME': env.str('DB_NAME'),
        'USER': env.str('DB_USER'),
        'PASSWORD': env.str('DB_PASSWORD'),
        'HOST': env.str('DB_HOST', 'localhost'),
        'PORT': env.str('DB_PORT', '5432'),
    }
}

# Authentication & Password validation

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

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Logging
LOGS_ENABLED = env.bool('LOGS_ENABLED', not DEBUG)
LOGS_ROOT = env.str('LOGS_DIR', root('logs'))
if LOGS_ROOT[:-1] != '/':
    LOGS_ROOT += '/'
if LOGS_ENABLED:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {pathname} func: {funcName} process:{process:d} thread:{thread:d} MESSAGE: {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'debug_file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOGS_ROOT + 'debug.log',
                'maxBytes': 1024 * 1024 * 5,  # 5 MB
                'backupCount': 10,
                'formatter': 'simple',
            },
            'info_file': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOGS_ROOT + 'info.log',
                'maxBytes': 1024 * 1024 * 5,  # 5 MB
                'backupCount': 10,
                'formatter': 'verbose'
            },
            'main_file': {
                'level': 'WARNING',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOGS_ROOT + 'main.log',
                'maxBytes': 1024 * 1024 * 5,  # 5 MB
                'backupCount': 10,
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'django': {
                'handlers': ['main_file'],
                'level': 'WARNING',
                'propagate': False,
            },
            'core': {
                'handlers': ['main_file'],
                'level': 'WARNING',
                'propagate': False,
            },
        },
    }

# Email
EMAIL_BACKEND = env.str('DJANGO_EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL", 'default@django.dev')
if env.str("DEFAULT_FROM_EMAIL", ""):
    EMAIL_HOST = env.str("EMAIL_HOST")
    EMAIL_PORT = env.str("EMAIL_PORT")
    EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
