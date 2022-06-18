from django.urls import path
from .views import *

urlpatterns = [
    path('get-disbursement/', braintree_disbursement, name='disbursement'),
    path('test-disbursement/', disbursement_test),
    path('populate-transactions', populate_transactions)
]
