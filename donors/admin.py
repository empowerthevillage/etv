from django.contrib import admin
from dashboard.models import dashboardModel

import csv
from django.http import HttpResponse

from .models import Donor, List
from donations.models import donation
from accounts.admin import admin_site

class DonorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'donor_level', 'donation_total', 'phone']
    list_filter = ['donor_level', 'category']
    search_fields = ['last_name', 'first_name', 'donor_level', 'email', 'donor_id', 'mailing_address']
    ordering = ['donor_level', 'last_name']
    actions = ['download_csv']
    
    def donation_total(self, obj):
        donor = Donor.objects.filter(id=obj.id).first()
        qs = donor.donations.all()
        sum = 0
        for x in qs:
            sum += x.amount
            string = str(sum)
            return str('$' + string)
    donation_total.short_descripton = 'Total Donations'

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
        
admin.site.register(Donor, DonorAdmin)
admin_site.register(Donor, DonorAdmin)
admin_site.register(List)

dashboardModel.objects.dash_register(Donor)