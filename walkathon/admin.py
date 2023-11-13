from django.contrib import admin, messages
from django.utils.translation import ngettext

import csv
from django.http import HttpResponse

from accounts.admin import admin_site

from .models import Walker, WalkerDonation, HomeGalleryImage, Organization, ShirtOrder, WalkerRegistrationPayment, WalkerPledgePayment, Sponsorship, OrgDonation

class WalkathonAdmin(admin.ModelAdmin):
    actions = ['set_active', 'set_inactive', 'download_csv']
    list_display = ['first_name', 'last_name', 'active', 'created']
    
    def set_active(self, request, queryset):
        updated = queryset.update(active=True)
        self.message_user(request, ngettext(
            '%d activated.', 
            '%d activated.', 
            updated,
        ) % updated, messages.SUCCESS)
    set_active.short_description = "Activate"
        
    def set_inactive(self, request, queryset):
        updated = queryset.update(active=False)
        self.message_user(request, ngettext(
            '%d deactivated.', 
            '%d deactivated.', 
            updated,
        ) % updated, messages.SUCCESS)
    set_inactive.short_description = "Deactivate"
    
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
    
class OrgAdmin(admin.ModelAdmin):
    actions = ['set_active', 'set_inactive', 'download_csv']
    list_display = ['title', 'active', 'created']
    
    def set_active(self, request, queryset):
        updated = queryset.update(active=True)
        self.message_user(request, ngettext(
            '%d activated.', 
            '%d activated.', 
            updated,
        ) % updated, messages.SUCCESS)
    set_active.short_description = "Activate"
        
    def set_inactive(self, request, queryset):
        updated = queryset.update(active=False)
        self.message_user(request, ngettext(
            '%d deactivated.', 
            '%d deactivated.', 
            updated,
        ) % updated, messages.SUCCESS)
    set_inactive.short_description = "Deactivate"
    
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

class WalkerDonationAdmin(admin.ModelAdmin):
    list_display = ['amount', 'walker', 'created']
    actions = ['download_csv']
    
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
    
class OrgDonationAdmin(admin.ModelAdmin):
    list_display = ['amount', 'organization', 'first_name','last_name', 'created']
    actions = ['download_csv']
    
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
    
class PledgeAdmin(admin.ModelAdmin):
    list_display = ['amount', 'walker', 'created']
    
class SponsorAdmin(admin.ModelAdmin):
    list_display = ['amount', 'first_name', 'last_name', 'created']

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['amount', 'walker', 'created']
    
admin_site.register(Walker, WalkathonAdmin)
admin_site.register(WalkerDonation, WalkerDonationAdmin)
admin_site.register(OrgDonation, OrgDonationAdmin)
admin_site.register(Sponsorship, SponsorAdmin)
admin_site.register(HomeGalleryImage)
admin_site.register(Organization)
admin_site.register(ShirtOrder)
admin_site.register(WalkerRegistrationPayment, RegistrationAdmin)
admin_site.register(WalkerPledgePayment, PledgeAdmin)
