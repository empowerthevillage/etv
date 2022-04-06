from django.contrib import admin
from dashboard.models import dashboardModel

from django.contrib import admin
from .models import donation_submission, donation, donation_event, tag
from accounts.admin import admin_site

class DonationAdmin(admin.ModelAdmin):
    list_display = ['amount', 'last_name', 'first_name', 'billing_profile', 'status', 'updated']
    list_filter = ['billing_profile', 'amount', 'frequency', 'status']
    search_fields = ['first_name', 'last_name', 'amount']
    ordering = ['-updated']
    

admin.site.register(donation_submission)
admin_site.register(donation, DonationAdmin)
admin_site.register(donation_event)
admin_site.register(tag)

dashboardModel.objects.dash_register(donation)