"""
Production Settings for Heroku
"""

import environ

from .production import *

env = environ.Env(
    DEBUG=(bool, False)
)

DEBUG = False

SECRET_KEY = env('SECRET_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_FACEBOOK_KEY = env('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = env('SOCIAL_AUTH_FACEBOOK_SECRET')
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
ALLOWED_HOSTS = ['etv.villageblackpages.org', 'www.etv.villageblackpages.org', 'etvlive.herokuapp.com', 'etv.empowerthevillage.org', 'www.etv.empowerthevillage.org', 'empowerthevillage.org', 'www.empowerthevillage.org', 'testing.empowerthevillage.org']
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_PORT = env('EMAIL_PORT')
MERCHANT_ID=env('MERCHANT_ID')
PUBLIC_KEY=env('PUBLIC_KEY')
PRIVATE_KEY=env('PRIVATE_KEY')
SHIPPO_KEY=env('SHIPPO_KEY')
GEOCODER_KEY=env('GEOCODER_KEY')
BRAINTREE_TOKENIZATION_KEY = env('TOKENIZATION_KEY')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

DATABASES = {
    'default': env.db(),
}
