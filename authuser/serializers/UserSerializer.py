from rest_framework import serializers
from authuser.models import User  # Ensure you are importing the right model
# from authuser.models import Role
class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'pass_key', 'phone', 'gm','secretary', 'role']


    def get_role(self, obj):
        """
        Get the first group name that the user belongs to.
        """
        group = obj.groups.first()  # Fetch the first group assigned to the user
        return group.name.lower() if group else None  # Return group name 

