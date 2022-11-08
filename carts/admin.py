from django.contrib import admin
from .models import *
from accounts.admin import admin_site

class ArtCartAdmin(admin.ModelAdmin):
    list_display = ['pk','timestamp', 'updated', 'active']
    
admin_site.register(Cart)
admin_site.register(FullGalleryCart, ArtCartAdmin)
admin_site.register(cartItem)
admin_site.register(TicketCart)
admin_site.register(ticketItem)
admin_site.register(ticketDonation)
admin_site.register(ticketAd)