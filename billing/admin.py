from django.contrib import admin

from .models import *
from accounts.admin import admin_site

admin.site.register(BillingProfile)
admin_site.register(BillingProfile)