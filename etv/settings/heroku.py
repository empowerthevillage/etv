"""
Production Settings for Heroku
"""

import environ

# If using in your own project, update the project namespace below
from .production import *

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# False if not in os.environ
DEBUG = False

# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_FACEBOOK_KEY = env('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = env('SOCIAL_AUTH_FACEBOOK_SECRET')
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
ALLOWED_HOSTS = ['etv.villageblackpages.org', 'www.etv.villageblackpages.org', 'etvlive.herokuapp.com', 'etv.empowerthevillage.org', 'www.etv.empowerthevillage.org', 'empowerthevillage.org', 'www.empowerthevillage.org']
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env('EMAIL_PORT')
MERCHANT_ID=env('MERCHANT_ID')
PUBLIC_KEY=env('PUBLIC_KEY')
PRIVATE_KEY=env('PRIVATE_KEY')
SHIPPO_KEY=env('SHIPPO_KEY')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
# Parse database connection url strings like psql://user:pass@127.0.0.1:8458/db
DATABASES = {
    # read os.environ['DATABASE_URL'] and raises ImproperlyConfigured exception if not found
    'default': env.db(),
}
