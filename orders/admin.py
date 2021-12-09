from django.contrib import admin
from .models import *
from accounts.admin import admin_site

class OrderAdmin(admin.ModelAdmin):
    list_display = ['braintree_id', 'billing_profile', 'formatted_total', 'status']
    list_filter = ['braintree_id', 'billing_profile', 'status']
    search_fields = ['braintree_id', 'billing_profile', 'status']
    ordering = ['updated', 'status']
    
    def formatted_total(self, obj):
        string = str(obj.total)
        formatted_total = str("$"+string)
        return formatted_total


admin_site.register(Order, OrderAdmin)
