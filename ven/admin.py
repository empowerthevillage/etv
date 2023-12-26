from django.contrib import admin
from accounts.admin import admin_site
from .models import Nomination, FamilyNomination, sponsor_img

from dashboard.models import dashboardModel

import csv
from django.http import HttpResponse

class VENAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'city', 'state', 'created']
    search_fields = ['business_name', 'owner_name', 'nominator_name', 'state', 'city', 'category', 'subcategory']
    ordering = ['business_name', 'city']
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
    
class VENFamilyAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state', 'created']
    search_fields = ['name',]
    ordering = ['created',]
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

admin_site.register(Nomination, VENAdmin)
admin_site.register(FamilyNomination, VENFamilyAdmin)
admin_site.register(sponsor_img)

dashboardModel.objects.dash_register(Nomination)
dashboardModel.objects.dash_register(FamilyNomination)
