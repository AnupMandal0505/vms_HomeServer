from rest_framework.serializers import ModelSerializer
from authuser.models import Snacks, SnacksItem,Order,OrderItem
from rest_framework import serializers
from authuser.models import User

class SnacksItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnacksItem
        fields = ["id", "name", "image"]

class SnacksSerializer(serializers.ModelSerializer):
    items = SnacksItemSerializer(many=True, source="SnacksItem")  # Using related_name

    class Meta:
        model = Snacks
        fields = ["id", "name", "items"]




class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orderitems = OrderItemSerializer(many=True, source="order_items")
    created_by_name = serializers.SerializerMethodField()
    created_by_phone = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "orderitems",
            "status",
            "created_by",         # still shows user ID
            "created_by_name",
            "created_by_phone",    
            "updated_by",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["id", "created_by", "updated_by", "created_at", "updated_at"]

    def get_created_by_name(self, obj):
        if obj.created_by:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}".strip()
        return None

    def get_created_by_phone(self, obj):
        return obj.created_by.phone if obj.created_by else None



