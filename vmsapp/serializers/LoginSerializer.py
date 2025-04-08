from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=128, write_only=True)
    role = serializers.CharField(max_length=50)

