from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin import AdminSite

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import MyUser, Team, Participant

class MyAdminSite(AdminSite):
    site_header = 'Empower The Village Administration'
    site_title = 'Admin'
    index_title = 'Empower The Village'
    login_template = 'accounts/adminlogin.html'
    index_template = 'admin/index.html'
    enable_nav_sidebar = True

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username','email', 'admin', 'rss_sponsor', 'bingo_sponsor', 'active')
    list_filter = ('admin', 'staff', 'team', 'rss_sponsor', 'bingo_sponsor')
    fieldsets = (
        ('Personal Information', {'fields': ('username','full_name', 'email', 'password', )}),
        ('Donation Information', {'fields': ('team', 'rss_sponsor', 'bingo_sponsor')}),
        ('Permissions', {'fields': ('admin','staff','active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2', 'team', 'rss_sponsor', 'bingo_sponsor', 'active')}
        ),
    )
    search_fields = ('username','email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(MyUser, UserAdmin)
admin.site.register(Team)
admin_site = MyAdminSite(name='myadmin')
admin_site.register(MyUser, UserAdmin)
admin_site.register(Team)
admin_site.register(Participant)
# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
