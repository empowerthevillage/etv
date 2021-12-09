from django.contrib import admin

from django.contrib import admin

from .models import Donor, List
from donations.models import donation
from accounts.admin import admin_site

class DonorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'donor_level', 'donation_total']
    list_filter = ['donor_level', 'category']
    search_fields = ['last_name', 'first_name', 'donor_level', 'email', 'donor_id', 'mailing_address']
    ordering = ['donor_level', 'last_name']

    def donation_total(self, obj):
        donor = Donor.objects.filter(id=obj.id).first()
        qs = donor.donations.all()
        sum = 0
        for x in qs:
            sum += x.amount
            string = str(sum)
            return str('$' + string)
    donation_total.short_descripton = 'Total Donations'

admin.site.register(Donor, DonorAdmin)
admin_site.register(Donor, DonorAdmin)
admin_site.register(List)