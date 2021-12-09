from django.contrib import admin
from .models import contact_submission
from accounts.admin import admin_site

admin_site.register(contact_submission)



