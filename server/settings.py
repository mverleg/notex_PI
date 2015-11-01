
from os.path import dirname, abspath, join
from package_versions import PACKAGE_NAME_PATTERN, PACKAGE_NAME_MESSAGE, VERSION_REST_PATTERN, \
	VERSION_PATTERN, VERSION_MESSAGE, FILENAME_PATTERN, FILENAME_MESSAGE, VERSION_MAX


BASE_DIR = dirname(dirname(abspath(__file__)))

AUTH_USER_MODEL = 'accounts.IndexUser'

PACKAGE_ZIP_DIR = join(BASE_DIR, 'package_zips')
PACKAGE_DIR = join(BASE_DIR, 'packages')

SITE_URL = 'http://localhost.markv.nl:8000/'
CDN_URL = 'http://localhost.markv.nl:8000/cdn'

SECRET_KEY = '@xe62(k2ayb7xh=ws!%h#ys%(sl^)tsk&v69q+y2@)yg6a9b9%'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'base',
	'accounts',
	'indx',
	'django_q',
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'base.unique_urls.WwwSlashMiddleware',
)

PREPEND_WWW = APPEND_SLASH = False  # see middleware
ROOT_URLCONF = 'urls'

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

WSGI_APPLICATION = 'wsgi.application'

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': join(BASE_DIR, 'data', 'db.sqlite3'),
	},
	'queue': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': join(BASE_DIR, 'data', 'queue.sqlite3'),
	}
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

Q_CLUSTER = {
	'name': 'package_index',
	'workers': 3,
	'compress': True,
	'label': 'Django Q',
	'orm': 'queue',
}


