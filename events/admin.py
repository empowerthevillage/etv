from tokenize import Single
from django.contrib import admin
from dashboard.models import dashboardModel
from django.utils.translation import ngettext
from django.contrib import messages

from .models import *
from accounts.admin import admin_site

import csv
from django.http import HttpResponse


class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date']
    search_fields = ['title', 'date']
    ordering = ['-date', 'title']
    

class ArtistAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'image']
    actions = ['mark_inactive']
    
    def mark_inactive(self, request, queryset):
        updated = queryset.update(active=False)
        self.message_user(request, ngettext(
            '%d artist successfully marked as inactive.', 
            '%d artists successfully marked as inactive.', 
            updated,
        ) % updated, messages.SUCCESS)
    mark_inactive.short_description = "Mark selected as inactive"
    
class TicketAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'event']
    actions = ['download_csv', 'mark_checkedin']
    search_fields = ['event', 'last_name']
    
    def mark_checkedin(self, request, queryset):
        updated = queryset.update(checked_in=True)
        self.message_user(request, ngettext(
            '%d listing successfully marked as checked in.', 
            '%d listings successfully marked as checked in.', 
            updated,
        ) % updated, messages.SUCCESS)
    mark_checkedin.short_description = "Mark selected as checked in"
    
    def download_csv(self, request, queryset):
        opts = queryset.model._meta
        model = queryset.model
        response = HttpResponse(content_type='text/csv')
        # force download.
        response['Content-Disposition'] = 'attachment;filename=export.csv'
        # the csv writer
        writer = csv.writer(response)
        field_names = [field.name for field in opts.fields]
        # Write a first row with header information
        writer.writerow(field_names)
        # Write data rows
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response
    download_csv.short_description = "Download selected as csv"

class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'event']
    actions = ['set_inactive']
    def set_inactive(self, request, queryset):
        updated = queryset.update(active=False)
        self.message_user(request, ngettext(
            '%d ticket marked as inactive',
            '%d ticket marked as inactive',
            updated,
        ) % updated, messages.SUCCESS)
    set_inactive.short_description = "Mark selected as inactive"

class ArtAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'price', 'description', 'width', 'height','active', 'sold', 'pre_sale']
    list_filter = ['artist', 'active']
    actions = ['make_presale', 'mark_inactive']
    def make_presale(self, request, queryset):
        updated = queryset.update(pre_sale=True)
        self.message_user(request, ngettext(
            '%d listing successfully marked as presale.', 
            '%d listings successfully marked as presale.', 
            updated,
        ) % updated, messages.SUCCESS)
    make_presale.short_description = "Mark selected as presale"
    
    def mark_inactive(self, request, queryset):
        updated = queryset.update(active=False)
        self.message_user(request, ngettext(
            '%d listing successfully marked as inactive.', 
            '%d listings successfully marked as inactive.', 
            updated,
        ) % updated, messages.SUCCESS)
    mark_inactive.short_description = "Mark selected as inactive"

class AuctionAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'image']
    
class CheckinAdmin(admin.ModelAdmin):
    list_display = ['time']
    actions = ['mark_inactive']
    def mark_inactive(self, request, queryset):
        updated = queryset.update(active=False)
        self.message_user(request, ngettext(
            '%d listing successfully marked as inactive.', 
            '%d listings successfully marked as inactive.', 
            updated,
        ) % updated, messages.SUCCESS)
    mark_inactive.short_description = "Mark selected as inactive"

class SignatureAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)
    
admin_site.register(Signature, SignatureAdmin)
admin_site.register(tag)
admin_site.register(Event, EventAdmin)
admin_site.register(SingleTicket, TicketAdmin)
admin_site.register(TicketType, TicketTypeAdmin)
admin_site.register(AddOn)
admin_site.register(Option)
admin_site.register(AdType)
admin_site.register(Ad)
admin_site.register(CheckIn, CheckinAdmin)
admin_site.register(CompleteDonation)
admin_site.register(GalleryItem)
admin_site.register(FullGalleryItem, ArtAdmin)
admin_site.register(AuctionItem, AuctionAdmin)
admin_site.register(Artist, ArtistAdmin)
admin_site.register(PhotoGalleryItem)
dashboardModel.objects.dash_register(Event)
dashboardModel.objects.dash_register(TicketType)
dashboardModel.objects.dash_register(SingleTicket)
dashboardModel.objects.dash_register(GalleryItem)
dashboardModel.objects.dash_register(Ad)
dashboardModel.objects.dash_register(CompleteDonation)