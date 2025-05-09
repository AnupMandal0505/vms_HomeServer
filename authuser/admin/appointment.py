# admin.py
from django.contrib import admin
from authuser.models import Appointment,AdditionalVisitor,RegularVisitor
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
    list_display = ('date', 'created_at','visitor_name','v_type', 'status', 'company_name')
    list_filter = ('status', 'date', 'company_name')  # Filters on the right
    search_fields = ('visitor_name', 'company_name', 'email', 'phone')  # Search box

    # Fieldsets for organizing fields in the admin panel
    fieldsets = (
        ('Visitor Information', {
            'fields': ('visitor_name', 'email', 'phone', 'visitor_img')
        }),
        ('Appointment Details', {
            'fields': ('date', 'description','v_type', 'status', 'purpose_of_visit')
        }),
        ('Company Details', {
            'fields': ('company_name', 'company_address')
        }),
        ('Assignment & Tracking', {
            'fields': ('gm','assigned_to', 'created_by', 'updated_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Hide timestamps by default
        }),
    )

    readonly_fields = ('created_at', 'updated_at')  # Make timestamps read-only







@admin.register(RegularVisitor)
class RegularVisitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'v_type', 'created_by', 'created_at')
    search_fields = ('name', 'phone', 'email', 'company_name')
    list_filter = ('v_type', 'created_at')

    fieldsets = (
        ("Visitor Info", {
            'fields': ('name', 'v_type', 'phone', 'email')
        }),
        ("Company Info", {
            'fields': ('company_name', 'company_address')
        }),
        ("Image Upload", {
            'fields': ('image',)
        }),
        ("Modification Meta", {
            'classes': ('collapse',),  # Optional: collapses this section
            'fields': ('created_by', 'created_at', 'updated_by', 'updated_at'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
