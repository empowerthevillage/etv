from django.contrib import admin
from .models import *
from django.utils.translation import ngettext
from django.contrib import messages
from accounts.admin import admin_site
from dashboard.models import dashboardModel

import csv
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
import geocoder

class VBPBook(admin.ModelAdmin):
    ordering = ['state']
    list_display = ['state', 'published']
    list_filter = ['published', 'state']
    actions = ['make_active', 'make_inactive', 'download_csv']
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

class VBPAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'approved', 'city', 'state', 'nominator_name']
    list_filter = ['approved', 'state', 'online_only', 'category', 'subcategory', 'nominator_name']
    search_fields = ['business_name', 'state', 'city', 'category', 'subcategory', 'nominator_name', 'nominator_email']
    ordering = ['state', 'business_name']
    actions = ['make_active', 'make_inactive', 'download_csv']
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
    
    def download_csv(modeladmin, request, queryset):
        if not request.user.is_staff:
            raise PermissionDenied
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

class VBPStateAdmin(admin.ModelAdmin):
    list_per_page = 500
    list_display = ['business_name', 'approved', 'website', 'category', 'city', 'updated', 'nominator_name']
    list_filter = ['county', 'city','approved', 'online_only', 'category', 'subcategory', 'team', 'nominator_name']
    search_fields = ['business_name', 'city', 'category', 'subcategory', 'user', 'nominator_name']
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
                geocode_result = geocoder.google(city+", NY", key='AIzaSyA1gqlqRGpMKsBiAKi9r0Q9b-v-BRDOL5k')
                county = geocode_result.current_result.county
                i.update(county=county)
    add_county.short_description = "Add county"

admin.site.register(vbp)
admin.site.register(vbp_book, VBPBook)
admin_site.register(vbp)
admin_site.register(vbp_book, VBPBook)
admin_site.register(mv_private)
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

dashboardModel.objects.dash_register(vbp_book)
dashboardModel.objects.dash_register(vbp_ct)
dashboardModel.objects.dash_register(vbp_dc)
dashboardModel.objects.dash_register(vbp_de)
dashboardModel.objects.dash_register(vbp_ma)
dashboardModel.objects.dash_register(vbp_md)
dashboardModel.objects.dash_register(vbp_nj)
dashboardModel.objects.dash_register(vbp_ny)
dashboardModel.objects.dash_register(vbp_oh)
dashboardModel.objects.dash_register(vbp_pa)
dashboardModel.objects.dash_register(vbp_va)
dashboardModel.objects.dash_register(vbp_al)
dashboardModel.objects.dash_register(vbp_ak)
dashboardModel.objects.dash_register(vbp_az)
dashboardModel.objects.dash_register(vbp_ca)
dashboardModel.objects.dash_register(vbp_ar)
dashboardModel.objects.dash_register(vbp_co)
dashboardModel.objects.dash_register(vbp_fl)
dashboardModel.objects.dash_register(vbp_ga)
dashboardModel.objects.dash_register(vbp_hi)
dashboardModel.objects.dash_register(vbp_id)
dashboardModel.objects.dash_register(vbp_il)
dashboardModel.objects.dash_register(vbp_in)
dashboardModel.objects.dash_register(vbp_ia)
dashboardModel.objects.dash_register(vbp_ks)
dashboardModel.objects.dash_register(vbp_ky)
dashboardModel.objects.dash_register(vbp_la)
dashboardModel.objects.dash_register(vbp_me)
dashboardModel.objects.dash_register(vbp_mi)
dashboardModel.objects.dash_register(vbp_mn)
dashboardModel.objects.dash_register(vbp_ms)
dashboardModel.objects.dash_register(vbp_mo)
dashboardModel.objects.dash_register(vbp_mt)
dashboardModel.objects.dash_register(vbp_ne)
dashboardModel.objects.dash_register(vbp_nv)
dashboardModel.objects.dash_register(vbp_nh)
dashboardModel.objects.dash_register(vbp_nm)
dashboardModel.objects.dash_register(vbp_nc)
dashboardModel.objects.dash_register(vbp_nd)
dashboardModel.objects.dash_register(vbp_ok)
dashboardModel.objects.dash_register(vbp_or)
dashboardModel.objects.dash_register(vbp_ri)
dashboardModel.objects.dash_register(vbp_sc)
dashboardModel.objects.dash_register(vbp_tn)
dashboardModel.objects.dash_register(vbp_tx)
dashboardModel.objects.dash_register(vbp_ut)
dashboardModel.objects.dash_register(vbp_vt)
dashboardModel.objects.dash_register(vbp_wa)
dashboardModel.objects.dash_register(vbp_wv)
dashboardModel.objects.dash_register(vbp_wi)
dashboardModel.objects.dash_register(vbp_wy)
