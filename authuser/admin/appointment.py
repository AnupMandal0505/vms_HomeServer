# admin.py
from django.contrib import admin
from authuser.models import Appointment,AdditionalVisitor
from django.utils.translation import gettext_lazy as _  # For translatable fieldset titles


class AdditionalVisitorInline(admin.TabularInline):  
    model = AdditionalVisitor
    extra = 1  
    can_delete = True  
    show_change_link = True  

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    inlines = [AdditionalVisitorInline]
    
    # Fields to display in list view
    list_display = ('date', 'created_at','visitor_name', 'status', 'company_name')
    list_filter = ('status', 'date', 'company_name')  # Filters on the right
    search_fields = ('visitor_name', 'company_name', 'email', 'phone')  # Search box

    # Fieldsets for organizing fields in the admin panel
    fieldsets = (
        ('Visitor Information', {
            'fields': ('visitor_name', 'email', 'phone', 'visitor_img')
        }),
        ('Appointment Details', {
            'fields': ('date', 'description', 'status', 'purpose_of_visit')
        }),
        ('Company Details', {
            'fields': ('company_name', 'company_address')
        }),
        ('Assignment & Tracking', {
            'fields': ('assigned_to', 'created_by', 'updated_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Hide timestamps by default
        }),
    )

    readonly_fields = ('created_at', 'updated_at')  # Make timestamps read-only

