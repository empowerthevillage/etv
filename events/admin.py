from tokenize import Single
from django.contrib import admin
from dashboard.models import dashboardModel
from django.utils.translation import ngettext
from django.contrib import messages

from .models import *
from accounts.admin import admin_site


class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date']
    search_fields = ['title', 'date']
    ordering = ['-date', 'title']

class ArtistAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'image']
    
class TicketAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'event']

class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'event']

class ArtAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'price', 'image', 'sold', 'pre_sale']
    actions = ['make_presale']
    def make_presale(self, request, queryset):
        updated = queryset.update(pre_sale=True)
        self.message_user(request, ngettext(
            '%d listing successfully marked as presale.', 
            '%d listings successfully marked as presale.', 
            updated,
        ) % updated, messages.SUCCESS)
    make_presale.short_description = "Mark selected VBP books as presale"

class AuctionAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'image']
                    
admin_site.register(tag)
admin_site.register(Event, EventAdmin)
admin_site.register(SingleTicket, TicketAdmin)
admin_site.register(TicketType, TicketTypeAdmin)
admin_site.register(AddOn)
admin_site.register(Option)
admin_site.register(AdType)
admin_site.register(Ad)
admin_site.register(CompleteDonation)
admin_site.register(GalleryItem, ArtAdmin)
admin_site.register(FullGalleryItem, ArtAdmin)
admin_site.register(AuctionItem, AuctionAdmin)
admin_site.register(Artist, ArtistAdmin)
dashboardModel.objects.dash_register(Event)
dashboardModel.objects.dash_register(TicketType)
dashboardModel.objects.dash_register(SingleTicket)
dashboardModel.objects.dash_register(GalleryItem)
dashboardModel.objects.dash_register(Ad)
dashboardModel.objects.dash_register(CompleteDonation)