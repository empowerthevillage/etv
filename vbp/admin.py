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

class VBPAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'approved', 'city', 'state']
    list_filter = ['approved', 'state', 'online_only', 'category', 'subcategory']
    search_fields = ['business_name', 'state', 'city', 'category', 'subcategory']
    ordering = ['state', 'business_name']
    actions = ['make_active', 'make_inactive']
    fieldsets = (
        (None, {
            'fields': ('business_name', 'website', 'category', 'subcategory', 'approved')
        }),
        ('Contact Information', {
            'fields': ('online_only', 'phone', 'phone_formatted', 'city', 'state', 'county',)
        }),
        ('Social Media', {
            'fields': ('instagram', 'facebook', 'twitter')
        }),
        ('Nominator Information', {
            'fields': ('nominator_name', 'nominator_email')
        }),
    )
    
    
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

class VBPStateAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'category', 'subcategory','approved', 'city', 'created',]
    list_filter = ['county', 'city','approved', 'online_only', 'category', 'subcategory', 'team']
    search_fields = ['business_name', 'city', 'category', 'subcategory', 'user']
    ordering = ['business_name']
    actions = ['make_active', 'make_inactive']
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
        response = HttpResponse(mimetype='text/csv')
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
                geocode_result = geocoder.google(city+", NY", key='AIzaSyA1gqlqRGpMKsBiAKi9r0Q9b-v-BRDOL5k')
                county = geocode_result.current_result.county
                i.update(county=county)
    add_county.short_description = "Add county"

admin.site.register(vbp)
admin.site.register(vbp_book)
admin_site.register(vbp)
admin_site.register(vbp_book, VBPBook)
admin_site.register(vbp_ct, VBPStateAdmin)
admin_site.register(vbp_dc, VBPStateAdmin)
admin_site.register(vbp_de, VBPStateAdmin)
admin_site.register(vbp_ma, VBPStateAdmin)
admin_site.register(vbp_md, VBPStateAdmin)
admin_site.register(vbp_nj, VBPStateAdmin)
admin_site.register(vbp_ny, VBPStateAdmin)
admin_site.register(vbp_oh, VBPStateAdmin)
admin_site.register(vbp_pa, VBPStateAdmin)
admin_site.register(vbp_va, VBPStateAdmin)
admin_site.register(vbp_al, VBPStateAdmin)
admin_site.register(vbp_ak, VBPStateAdmin)
admin_site.register(vbp_az, VBPStateAdmin)
admin_site.register(vbp_ca, VBPStateAdmin)
admin_site.register(vbp_ar, VBPStateAdmin)
admin_site.register(vbp_co, VBPStateAdmin)
admin_site.register(vbp_fl, VBPStateAdmin)
admin_site.register(vbp_ga, VBPStateAdmin)
admin_site.register(vbp_hi, VBPStateAdmin)
admin_site.register(vbp_id, VBPStateAdmin)
admin_site.register(vbp_il, VBPStateAdmin)
admin_site.register(vbp_in, VBPStateAdmin)
admin_site.register(vbp_ia, VBPStateAdmin)
admin_site.register(vbp_ks, VBPStateAdmin)
admin_site.register(vbp_ky, VBPStateAdmin)
admin_site.register(vbp_la, VBPStateAdmin)
admin_site.register(vbp_me, VBPStateAdmin)
admin_site.register(vbp_mi, VBPStateAdmin)
admin_site.register(vbp_mn, VBPStateAdmin)
admin_site.register(vbp_ms, VBPStateAdmin)
admin_site.register(vbp_mo, VBPStateAdmin)
admin_site.register(vbp_mt, VBPStateAdmin)
admin_site.register(vbp_ne, VBPStateAdmin)
admin_site.register(vbp_nv, VBPStateAdmin)
admin_site.register(vbp_nh, VBPStateAdmin)
admin_site.register(vbp_nm, VBPStateAdmin)
admin_site.register(vbp_nc, VBPStateAdmin)
admin_site.register(vbp_nd, VBPStateAdmin)
admin_site.register(vbp_ok, VBPStateAdmin)
admin_site.register(vbp_or, VBPStateAdmin)
admin_site.register(vbp_ri, VBPStateAdmin)
admin_site.register(vbp_sc, VBPStateAdmin)
admin_site.register(vbp_tn, VBPStateAdmin)
admin_site.register(vbp_tx, VBPStateAdmin)
admin_site.register(vbp_ut, VBPStateAdmin)
admin_site.register(vbp_vt, VBPStateAdmin)
admin_site.register(vbp_wa, VBPStateAdmin)
admin_site.register(vbp_wv, VBPStateAdmin)
admin_site.register(vbp_wi, VBPStateAdmin)
admin_site.register(vbp_wy, VBPStateAdmin)

