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
    orderitems = OrderItemSerializer(many=True, source="SnacksItem")

    class Meta:
        model = Order
        fields = ["id", "orderitems", "status", "created_by", "updated_by", "created_at", "updated_at"]
        read_only_fields = ["id", "created_by", "updated_by", "created_at", "updated_at"]



