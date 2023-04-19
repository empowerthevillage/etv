from django.contrib import admin
from accounts.admin import admin_site
from .models import Walker, WalkerDonation, HomeGalleryImage, Organization, ShirtOrder, WalkerRegistrationPayment, OrgDonation

admin_site.register(Walker)
admin_site.register(WalkerDonation)
admin_site.register(OrgDonation)
admin_site.register(HomeGalleryImage)
admin_site.register(Organization)
admin_site.register(ShirtOrder)
admin_site.register(WalkerRegistrationPayment)
