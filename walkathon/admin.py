from django.contrib import admin
from accounts.admin import admin_site
from .models import Walker, WalkerDonation, HomeGalleryImage

admin_site.register(Walker)
admin_site.register(WalkerDonation)
admin_site.register(HomeGalleryImage)
