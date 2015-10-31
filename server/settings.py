
from os.path import dirname, abspath, join


BASE_DIR = dirname(dirname(abspath(__file__)))

AUTH_USER_MODEL = 'accounts.IndexUser'

PACKAGE_DIR = join(BASE_DIR, 'packages')

PACKAGE_NAME_PATTERN = r'[a-zA-Z][a-zA-Z0-9_.]*'

INDEX_URL = 'http://localhost.markv.nl/index'
CDN_URL = 'http://localhost.markv.nl/cdn'

FILENAME_PATTERN = r'[a-zA-Z0-9_\-.]{1,32}'
FILENAME_MESSAGE = 'File and directory names may have a length up to 32 ' + \
	'selected from alphanumeric characters, periods, dashes and underscores.'  # the 32 is the chosen db limit

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
	'pindex',
	'indx',
	'statcdn',
	'upld',
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
	}
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
