from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authuser.models import User
from django.utils.translation import gettext_lazy as _


# CustomUser Admin Configuration
class CustomUserAdmin(UserAdmin):
    model = User
    # Define the fieldsets for the admin form layout
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'pass_key')}),
        (("Group"), {"fields": ("groups","user_permissions")}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Team info'), {'fields': ('gm',)}),
    )
    
    # List display settings
    list_display = ('phone', 'first_name', 'email','get_groups', 'is_staff', 'is_active', 'date_joined')
    
    # Search fields
    search_fields = ('phone', 'first_name', 'last_name', 'email')
    
    # Add filter for 
    list_filter = ('is_staff', 'is_active')

    # Define what fields are required for creating a user
    add_fieldsets = (
        (None, {'fields': ('phone', 'password1', 'password2','pass_key')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    # Update ordering to use 'phone' instead of 'username'
    ordering = ('phone',)


 # Custom method to display groups in list view
    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])  # Return group names as a string
    
    get_groups.short_description = "Groups"  # Custom column name

# Register the CustomUser model with the custom admin
admin.site.register(User, CustomUserAdmin)





















from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()

class UserInline(admin.TabularInline):
    model = User.groups.through  # This is the intermediate model for the ManyToManyField
    extra = 0
    verbose_name = "User"
    verbose_name_plural = "Users"

class GroupAdmin(BaseGroupAdmin):
    inlines = [UserInline]

# Unregister the default Group admin and register your customized one
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
