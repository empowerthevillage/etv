from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', cart_home, name='home'),
    path('checkout', checkout_home, name='checkout'),
    path('checkout-confirm', checkout_confirm, name='checkout-confirm'),
    path('checkout-done', checkout_done, name="checkout-done"),
    path('checkout-update', checkout_new_update, name='new-update'),
    path('checkout-saved-update', checkout_saved_update, name='saved-update'),
    path('nsnb-update', nsnb_update, name='nsnb-update'),
    path('nssb-update', nssb_update, name='nssb-update'),
    path('ssnb-update', ssnb_update, name='ssnb-update'),
    path('sssb-update', sssb_update, name='sssb-update'),
    path('charge', new_charge, name="charge"),
    path('update-cart', ajaxUpdateItems, name="ajax-update"),
    path('remove-items',ajaxRemoveItems, name='ajax-remove'),
]
