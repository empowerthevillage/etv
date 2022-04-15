from django.contrib import admin
from .models import contact_submission
from accounts.admin import admin_site
from dashboard.models import dashboardModel

admin_site.register(contact_submission)

dashboardModel.objects.dash_register(contact_submission)

