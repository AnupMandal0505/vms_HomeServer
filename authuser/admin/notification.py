from django.contrib import admin
from authuser.models import CallNotification

@admin.register(CallNotification)
class CallNotificationAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "created_at","updated_at", "read")
    list_filter = ("read", "created_at")
    search_fields = ("sender__username", "receiver__username")
    ordering = ("-created_at",)