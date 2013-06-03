import os
import sys
import platform
import djcelery

djcelery.setup_loader()

from django.contrib.messages import constants as messages

# ===========================
# = Directory Declaractions =
# ===========================

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

CURRENT_DIR   = os.path.dirname(__file__)
TEMPLATE_DIRS = (os.path.join(CURRENT_DIR, 'templates'),)
UTILS_ROOT    = os.path.join(CURRENT_DIR, 'utils')
APPS_ROOT   = os.path.join(CURRENT_DIR, 'apps')

if '/utils' not in ' '.join(sys.path):
    sys.path.append(UTILS_ROOT)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (('Tyler Rilling', 'tyler@underlost.net'))
MANAGERS = ADMINS

#DB info injected by Heroku
import dj_database_url
DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

#Global Settings

BROKER_HOST = "localhost"
#BROKER_PORT = 5672
#BROKER_USER = "guest"
#BROKER_PASSWORD = "guest"
#BROKER_VHOST = "/"

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME')
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD')
EMAIL_PORT = "25"
#EMAIL_USE_TLS = True

#Amazon S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3.S3Storage'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = 'fir3ball'

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

SITE_NAME = 'fireball'
ALLOW_NEW_REGISTRATIONS = True
PUBLIC = True
#COMPRESS_ENABLED = True

AUTH_USER_MODEL = 'core.Profile'

MEDIA_ROOT = os.path.join(SITE_ROOT, 'media/')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(SITE_ROOT, 'static/')
STATIC_URL = '/static/'
STATICFILES_DIRS = ()

WSGI_APPLICATION = 'fireball.wsgi.application'

INTERNAL_IPS = ['127.0.0.1']
MESSAGE_TAGS = {
    messages.WARNING: 'alert',
    messages.ERROR: 'alert alert-error',
    messages.SUCCESS: 'alert alert-success',
    messages.INFO: 'alert alert-info',
}

API_LIMIT_PER_PAGE = 25

# ===========================
# = Django-specific Modules =
# ===========================

SECRET_KEY = 'wzqxrx6a7a=2a^ubw$_a_ozah+cvtslmx81f$8ecfdmgk=wtty'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'fireball.core.middleware.Public',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "fireball.core.context_processors.template_settings",
)


ROOT_URLCONF = 'fireball.urls'

TEMPLATE_DIRS = (
	os.path.join(SITE_ROOT, 'templates')
)

INSTALLED_APPS = (

	#Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.comments',

    #Prancing on Heroku
    'djcelery',
    'gunicorn',
    'south',
    'storages',
    'compressor',
    'taggit',

    #Internal
    'fireball.core',
    'fireball.blobs',
    'fireball.api',
    
)