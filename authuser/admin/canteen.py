from django.contrib import admin
from authuser.models import  Snacks, SnacksItem, Order,OrderItem


# Format Snacks category
@admin.register(Snacks)
class SnacksAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

# Format SnacksItem display
@admin.register(SnacksItem)
class SnacksItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    list_filter = ("category",)
    search_fields = ("name", "category__name")

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50"/>'
        return "No Image"
    image_preview.allow_tags = True
    image_preview.short_description = "Image"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_by", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at")
    search_fields = ("created_by__username",)
    ordering = ("-created_at",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order")  

