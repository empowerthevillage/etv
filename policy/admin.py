from django.contrib import admin
from accounts.admin import admin_site
from .models import Flyer, VillageStriversApplication

admin_site.register(Flyer)
admin_site.register(VillageStriversApplication)