from django.contrib import admin
from accounts.admin import admin_site
from .models import *

class AddressAdmin(admin.ModelAdmin):
    list_display = ['billing_profile', 'address_line_1', 'address_type']
    list_filter = ['billing_profile', 'address_line_1', 'address_type']
    search_fields = ['billing_profile', 'address_line_1', 'address_type']
    ordering = ['address_type']
    
admin_site.register(Address, AddressAdmin)
