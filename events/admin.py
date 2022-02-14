from django.contrib import admin

from .models import *
from accounts.admin import admin_site


class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date']
    search_fields = ['title', 'date']
    ordering = ['-date', 'title']

class TicketAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'event']

class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'event']

admin_site.register(tag)
admin_site.register(Event, EventAdmin)
admin_site.register(SingleTicket)
admin_site.register(TicketType, TicketTypeAdmin)
admin_site.register(AddOn)
admin_site.register(Option)
