from django.urls import path
from .views import *

urlpatterns = [
    path('', cart_home, name='home'),
    path('add-nonce-merch', add_nonce_to_merch, name='add-nonce-merch'),
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
    path('ticket-nb', ticket_nb, name='ticket-nb'),
    path('gallery-update', gallery_cart_update, name='gallery-update'),
    path('gallery-remove', gallery_cart_remove, name='gallery-remove'),
    path('presale-checkout', gallery_sale, name="gallery-checkout"),
    path('full-gallery-update', full_gallery_cart_update, name='full-gallery-update'),
    path('full-gallery-remove', full_gallery_cart_remove, name='full-gallery-remove'),
    path('full-gallery-checkout', full_gallery_sale, name="full-gallery-checkout"),
    path('make-art-disb', gallery_make_disbursement),
    path('make-don-disb', donation_make_disbursement)
]
