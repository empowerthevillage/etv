from django.contrib import admin

from .models import *
from accounts.admin import admin_site


class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date']
    search_fields = ['title', 'date']
    ordering = ['-date', 'title']

class TicketAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'event']

admin_site.register(tag)
admin_site.register(Event, EventAdmin)
admin_site.register(SingleTicket)
admin_site.register(TicketType)
admin_site.register(AddOn)
admin_site.register(Option)
