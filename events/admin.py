from tokenize import Single
from django.contrib import admin
from dashboard.models import dashboardModel

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
admin_site.register(SingleTicket, TicketAdmin)
admin_site.register(TicketType, TicketTypeAdmin)
admin_site.register(AddOn)
admin_site.register(Option)
admin_site.register(AdType)
admin_site.register(Ad)
admin_site.register(CompleteDonation)
dashboardModel.objects.dash_register(Event)
dashboardModel.objects.dash_register(TicketType)
dashboardModel.objects.dash_register(SingleTicket)
dashboardModel.objects.dash_register(Ad)
dashboardModel.objects.dash_register(CompleteDonation)