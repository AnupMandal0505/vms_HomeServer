from authuser.models import User
from authuser.models import CallNotification
from rest_framework import serializers



class ContactListSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'first_name','last_name','role']

    def get_role(self, obj):
        """
        Get the first group name that the user belongs to.
        """
        group = obj.groups.first()  # Fetch the first group assigned to the user
        return group.name.lower() if group else None  # Return group name 




class CallNotificationSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()
    sender_name = serializers.SerializerMethodField()
    sender_role = serializers.SerializerMethodField()  

    id = serializers.UUIDField(format='hex')  # Ensures UUID is serialized as a string

    class Meta:
        model = CallNotification
        fields = ['id','sender_name','sender_role', 'read', 'sender', 'receiver']

    def get_sender(self, obj):
        return obj.sender.phone  # Use sender's phone number instead of UUID

    def get_receiver(self, obj):
        return str(obj.receiver)  # Use receiver's phone number
    
    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}".strip()  # First name + Last name

    def get_sender_role(self, obj):
        group = obj.sender.groups.first()  # ✅ Sirf pehla group fetch karega
        return group.name if group else None
