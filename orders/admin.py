from django.contrib import admin
from .models import *
from accounts.admin import admin_site
from dashboard.models import dashboardModel

import csv
from django.http import HttpResponse

class OrderAdmin(admin.ModelAdmin):
    list_display = ['braintree_id', 'billing_profile', 'formatted_total', 'status']
    list_filter = ['braintree_id', 'billing_profile', 'status']
    search_fields = ['braintree_id', 'billing_profile', 'status']
    ordering = ['updated', 'status']
    
    def formatted_total(self, obj):
        string = str(obj.total)
        formatted_total = str("$"+string)
        return formatted_total

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

class LOAAdmin(admin.ModelAdmin):
    list_display = ['braintree_id']
    actions = ['download_csv']
    filter_horizontal: ('items')
    
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

admin_site.register(Order, OrderAdmin)
admin_site.register(LOAArtPurchase, LOAAdmin)
dashboardModel.objects.dash_register(LOAPresalePurchase)
