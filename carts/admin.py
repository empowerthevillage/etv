from django.contrib import admin
from .models import *
from accounts.admin import admin_site
from django.utils.translation import ngettext
from django.contrib import messages

class ArtCartAdmin(admin.ModelAdmin):
    list_display = ['pk','timestamp', 'updated', 'active']
    
class TicketAdmin(admin.ModelAdmin):
    list_display = ['pk','timestamp','get_items','active']
    actions = ['set_inactive']
    list_per_page = 500
    
    @admin.display(ordering='book__author', description='Author')
    def get_items(self, obj):
        items = ticketItem.objects.filter(cart=obj)
        return str(items)
    
    def set_inactive(self, request, queryset):
        updated = queryset.update(active=False)
        self.message_user(request, ngettext(
            '%d ticket marked as inactive',
            '%d ticket marked as inactive',
            updated,
        ) % updated, messages.SUCCESS)
    set_inactive.short_description = "Mark selected as inactive"
    
admin_site.register(Cart)
admin_site.register(FullGalleryCart, ArtCartAdmin)
admin_site.register(cartItem)
admin_site.register(TicketCart, TicketAdmin)
admin_site.register(ticketItem)
admin_site.register(ticketDonation)
admin_site.register(ticketAd)