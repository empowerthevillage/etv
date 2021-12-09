from django.contrib import admin

from .models import *
from accounts.admin import admin_site


class newInventoryAdmin(admin.ModelAdmin):
    list_display = ['sku', 'product', 'variation', 'quantity']
    list_filter = ['product', 'variation']
    search_fields = ['product', 'variation']
    ordering = ['product', 'variation']

admin_site.register(size)
admin_site.register(color)
admin_site.register(image)
admin_site.register(Variation)
admin_site.register(newProduct)
admin_site.register(newInventory, newInventoryAdmin)