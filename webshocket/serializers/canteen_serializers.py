from rest_framework.serializers import ModelSerializer
from authuser.models import Order,OrderItem
from rest_framework import serializers
from authuser.models import User
from django.utils.timezone import localtime


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details in the order response."""
    class Meta:
        model = User
        fields = ["phone","first_name","last_name"]  # Add other fields if needed


# class GetOrderSerializer(serializers.ModelSerializer):
#     """Serializer for Order, including user details."""
#     created_by = UserSerializer(read_only=True)
#     updated_by = UserSerializer(read_only=True)

#     class Meta:
#         model = Order
#         fields = '__all__'

#         def to_representation(self, instance):
#                 data = super().to_representation(instance)
#                 if instance.created_at:
#                     data["created_at"] = localtime(instance.created_at).strftime("%Y-%m-%d %H:%M:%S")
#                 if instance.updated_at:
#                     data["updated_at"] = localtime(instance.updated_at).strftime("%Y-%m-%d %H:%M:%S")

#                 return data



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class GetOrderSerializer(serializers.ModelSerializer):
    orderitems = OrderItemSerializer(many=True, source="order_items")
    created_by_name = serializers.SerializerMethodField()
    created_by_phone = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "orderitems",
            "status",
            "created_by_name",
            "created_by_phone",    
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_created_by_name(self, obj):
        if obj.created_by:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}".strip()
        return None

    def get_created_by_phone(self, obj):
        return obj.created_by.phone if obj.created_by else None



