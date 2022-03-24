from django.contrib import admin
from accounts.admin import admin_site
from .models import Nomination, FamilyNomination

class VENAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'city', 'state']
    search_fields = ['business_name', 'owner_name', 'nominator_name', 'state', 'city', 'category', 'subcategory']
    ordering = ['business_name', 'city']

admin_site.register(Nomination, VENAdmin)
admin_site.register(FamilyNomination)
