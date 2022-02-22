from django.contrib import admin
from .models import *
from django.utils.translation import ngettext
from django.contrib import messages
from accounts.admin import admin_site
import csv
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
import geocoder

class VBPBook(admin.ModelAdmin):
    list_display = ['state', 'published']
    list_filter = ['published', 'state']
    def make_active(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, ngettext(
            '%d listing successfully marked as approved.', 
            '%d listings successfully marked as approved.', 
            updated,
        ) % updated, messages.SUCCESS)
    make_active.short_description = "Mark selected VBP books as approved"

    def make_inactive(self, request, queryset):
        updated = queryset.update(approved=False)
        self.message_user(request, ngettext(
            '%d listing successfully marked as not yet approved.', 
            '%d listings successfully marked as not yet approved.', 
            updated,
        ) % updated, messages.SUCCESS)
    make_inactive.short_description = "Mark selected VBP books as not approved"

class VBPStateAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'approved', 'website', 'category', 'city', 'state']
    list_filter = ['county', 'city', 'state', 'approved', 'online_only', 'category', 'subcategory']
    search_fields = ['business_name', 'city', 'state', 'category', 'subcategory', 'user']
    ordering = ['-updated', 'business_name']
    actions = ['make_active', 'make_inactive', 'download_csv']
    fieldsets = (
        (None, {
            'fields': ('business_name', 'website', 'category', 'subcategory', 'approved')
        }),
        ('Contact Information', {
            'fields': ('online_only', 'phone', 'city', 'county',)
        }),
        ('Social Media', {
            'fields': ('instagram', 'facebook', 'twitter')
        }),
        ('Nominator Information', {
            'fields': ('nominator_name', 'nominator_email', 'nominator_owner', 'nominator_recommended', 'user', 'team')
        }),
    )
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

    def make_active(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, ngettext(
            '%d listing successfully marked as approved.', 
            '%d listings successfully marked as approved.', 
            updated,
        ) % updated, messages.SUCCESS)
    make_active.short_description = "Mark selected submissions as approved"

    def make_inactive(self, request, queryset):
        updated = queryset.update(approved=False)
        self.message_user(request, ngettext(
            '%d listing successfully marked as not yet approved.', 
            '%d listings successfully marked as not yet approved.', 
            updated,
        ) % updated, messages.SUCCESS)
    make_inactive.short_description = "Mark selected submissions as not approved"

    def add_county(self, request, queryset):
        for i in queryset:
            if not i.county:
                city = i.city
                state = i.state
                geocode_result = geocoder.google(city+","+state, key='AIzaSyA1gqlqRGpMKsBiAKi9r0Q9b-v-BRDOL5k')
                county = geocode_result.current_result.county
                i.update(county=county)
    add_county.short_description = "Add county"

admin_site.register(vbpus_book, VBPBook)
admin_site.register(vbpus)