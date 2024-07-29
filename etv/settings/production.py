import os
import environ
import psycopg2
from pathlib import Path
import dj_database_url
import braintree
db_from_env = dj_database_url.config(conn_max_age=500)

env = environ.Env(
    DEBUG=(bool, False)
)
DATABASES = { 'default': dj_database_url.config() }

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


braintree_merchant_id = env('MERCHANT_ID')
braintree_public = env('PUBLIC_KEY')
braintree_private = env('PRIVATE_KEY')
BRAINTREE_TOKENIZATION_KEY = env('TOKENIZATION_KEY')

GATEWAY = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Production,
        merchant_id = braintree_merchant_id,
        public_key = braintree_public,
        private_key = braintree_private,
    )
)
braintree_merchant_id_production = env('ID_PRODUCTION')
braintree_public_production = env('PKEY_PRODUCTION')
braintree_private_production = env('PRKEY_PRODUCTION')
GATEWAY_PUBLIC = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Production,
        merchant_id = braintree_merchant_id_production,
        public_key = braintree_public_production,
        private_key = braintree_private_production,
    )
)
SECRET_KEY = env('SECRET_KEY')
RECAPTCHA = env('RECAPTCHA')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_FACEBOOK_KEY = env('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = env('SOCIAL_AUTH_FACEBOOK_SECRET')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
MAILCHIMP_API_KEY = env('MAILCHIMP_API_KEY')

SHIPPO_KEY = env('SHIPPO_KEY')

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')

GEOCODER_KEY = env('GEOCODER_KEY')
GOOGLE_API_KEY = env('GEOCODER_KEY')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

DEBUG = True

ALLOWED_HOSTS = ['.empowerthevillage.org', '.villageblackpages.org', '.herokuapp.com']

SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'accounts',
    'address',
    'addresses',
    'bfchallenge',
    'billing',
    'carts',
    'content',
    'ckeditor',
    'dashboard',
    'donations',
    'donors',
    'django_quill',
    'etv',
    'education',
    'events',
    'health',
    'merchandise',
    'orders',
    'policy',
    'prosperity',
    'phone_field',
    'scraper',
    'social_django',
    'sweetify',
    'storages',
    'tinymce',
    'walkathon',
    'whitenoise.runserver_nostatic',
    'vbp',
    'vbpus',
    'ven',
]

AUTH_USER_MODEL = 'accounts.MyUser'

LOGIN_URL = '/login/'
LOGIN_URL_REDIRECT = '/'
LOUGOUT_REDIRECT_URL = 'login'

TINYMCE_DEFAULT_CONFIG = {
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft | code"
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'etv.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(BASE_DIR / 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'etv.context_processors.add_login_form',
            ],
        },
    },
]

SWEETIFY_SWEETALERT_LIBRARY = 'sweetalert2'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
)

SOCIAL_AUTH_STRATEGY = 'social_django.strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social_django.models.DjangoStorage'
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

WSGI_APPLICATION = 'etv.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}
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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


BASE_DIR = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_my_proj"),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = True

AWS_S3_CUSTOM_DOMAIN = 'etv-static.s3.amazonaws.com'
AWS_LOCATION = 'static'

DEFAULT_FILE_STORAGE = 'etv.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'etv.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'etv-static'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static-cdn", "media_root")
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
import datetime

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
AWS_HEADERS = { 
	'Expires': expires,
	'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SECURE_CROSS_ORIGIN_OPENER_POLICY='same-origin-allow-popups'