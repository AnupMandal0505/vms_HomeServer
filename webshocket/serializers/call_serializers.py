from rest_framework.serializers import ModelSerializer
from authuser.models import User
from authuser.models import CallNotification
from rest_framework import serializers
from django.contrib.auth.models import Group


class CallNotificationSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()
    sender_name = serializers.SerializerMethodField()
    sender_id = serializers.SerializerMethodField()
    sender_role = serializers.SerializerMethodField()


    class Meta:
        model = CallNotification
        fields = ['id','sender_id','sender_name','sender_role', 'read', 'sender', 'receiver']

    def get_sender(self, obj):
        return obj.sender.phone  # Use sender's phone number instead of UUID

    def get_receiver(self, obj):
        return str(obj.receiver.id)  # Use receiver's phone number
    
    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}".strip()  # First name + Last name

    def get_sender_id(self, obj):
        return str(obj.sender.id)

    def get_sender_role(self, obj):
        group = obj.sender.groups.first()  # ✅ Sirf pehla group fetch karega
        return group.name if group else None
