from django.contrib import admin

from .models import *
from accounts.admin import admin_site


class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date']
    search_fields = ['title', 'date']
    ordering = ['-date', 'title']

admin_site.register(tag)
admin_site.register(Event, EventAdmin)
