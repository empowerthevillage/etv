from django.contrib import admin, messages
from django.utils.translation import ngettext

import csv
from django.http import HttpResponse

from accounts.admin import admin_site

from .models import Walker, WalkerDonation, HomeGalleryImage, Organization, ShirtOrder, WalkerRegistrationPayment, WalkerPledgePayment, Sponsorship, OrgDonation

class WalkathonAdmin(admin.ModelAdmin):
    actions = ['set_500', 'download_csv']
    
    def set_500(self, request, queryset):
        updated = queryset.update(donation_goal=500)
        self.message_user(request, ngettext(
            '%d goal changed.', 
            '%d goals changed.', 
            updated,
        ) % updated, messages.SUCCESS)
    set_500.short_description = "Set goal to $500"
    
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
