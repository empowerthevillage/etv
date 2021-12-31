from django.contrib import admin
from accounts.admin import admin_site
from .models import *

class ScraperAdmin(admin.ModelAdmin):
    list_display = ['name', 'website']

admin_site.register(VBPScraped, ScraperAdmin)
