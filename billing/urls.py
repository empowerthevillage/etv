from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('get-disbursement/', braintree_disbursement, name='disbursement'),
]
