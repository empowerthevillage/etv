from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('get_disbursement', braintree_disbursement, name='disbursement'),
]
