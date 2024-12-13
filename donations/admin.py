from django.contrib import admin
from dashboard.models import dashboardModel

from django.contrib import admin

from decimal import Decimal, InvalidOperation

from .models import donation_submission, donation, donation_event, tag
from accounts.admin import admin_site

import csv
from django.http import HttpResponse

class DonationAdmin(admin.ModelAdmin):
    list_display = ['sanitized_amount', 'last_name', 'first_name', 'billing_profile', 'status', 'updated']
    list_filter = ['billing_profile', 'amount', 'frequency', 'status']
    search_fields = ['first_name', 'last_name', 'amount']
    ordering = ['-updated']
    actions = ['download_csv']

    def sanitized_amount(self, obj):
        """Display sanitized amount in the admin."""
        return obj.sanitized_amount
    sanitized_amount.short_description = "Amount (Sanitized)"  # Column header in the admin

    def download_csv(self, request, queryset):
        """Allow CSV download."""
        opts = queryset.model._meta
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename=export.csv'
        writer = csv.writer(response)
        field_names = [field.name for field in opts.fields]
        writer.writerow(field_names)  # Header row
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response
    download_csv.short_description = "Download selected as CSV"
    

admin.site.register(donation_submission)
admin_site.register(donation, DonationAdmin)
admin_site.register(donation_event)
admin_site.register(tag)

dashboardModel.objects.dash_register(donation)