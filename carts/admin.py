from django.contrib import admin
from .models import *
from accounts.admin import admin_site

admin_site.register(TicketCart)
admin_site.register(ticketItem)