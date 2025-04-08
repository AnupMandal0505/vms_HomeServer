from rest_framework.serializers import ModelSerializer
from authuser.models import Order
from rest_framework import serializers
from authuser.models import User
from django.utils.timezone import localtime


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details in the order response."""
    class Meta:
        model = User
        fields = ["phone","first_name","last_name"]  # Add other fields if needed


class GetOrderSerializer(serializers.ModelSerializer):
    """Serializer for Order, including user details."""
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

        def to_representation(self, instance):
                data = super().to_representation(instance)
                if instance.created_at:
                    data["created_at"] = localtime(instance.created_at).strftime("%Y-%m-%d %H:%M:%S")
                if instance.updated_at:
                    data["updated_at"] = localtime(instance.updated_at).strftime("%Y-%m-%d %H:%M:%S")

                return data