from django.contrib import admin, messages
from django.utils.translation import ngettext

from accounts.admin import admin_site

from .models import Walker, WalkerDonation, HomeGalleryImage, Organization, ShirtOrder, WalkerRegistrationPayment, WalkerPledgePayment, OrgDonation

class WalkathonAdmin(admin.ModelAdmin):
    actions = ['set_500',]
    def set_500(self, request, queryset):
        updated = queryset.update(donation_goal=500)
        self.message_user(request, ngettext(
            '%d goal changed.', 
            '%d goals changed.', 
            updated,
        ) % updated, messages.SUCCESS)
    set_500.short_description = "Set goal to $500"

admin_site.register(Walker, WalkathonAdmin)
admin_site.register(WalkerDonation)
admin_site.register(OrgDonation)
admin_site.register(HomeGalleryImage)
admin_site.register(Organization)
admin_site.register(ShirtOrder)
admin_site.register(WalkerRegistrationPayment)
admin_site.register(WalkerPledgePayment)
