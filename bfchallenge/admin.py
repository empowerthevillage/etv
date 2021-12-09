from django.contrib import admin

from accounts.models import Participant
from .models import *
from accounts.admin import admin_site

class RSSAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'team', 'first_name', 'last_name', 'user', 'amount', 'date', 'industry', 'submitted']
    list_filter = ['team', 'industry']
    search_fields = ['user', 'team', 'amount', 'date', 'business_name', 'industry']
    ordering = ['team', 'submitted']
    
class NominationAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'team', 'user', 'state', 'submitted']
    list_filter = ['team', 'state']
    search_fields = ['user', 'team', 'business_name', 'state']
    ordering = ['team', 'submitted']

admin.site.register(bingo_card)
admin.site.register(user_bingo_card)
admin_site.register(user_bingo_form)
admin_site.register(bingo_card)
admin_site.register(user_bingo_card)
admin_site.register(readysetshop_transaction, RSSAdmin)
admin_site.register(nomination, NominationAdmin)


