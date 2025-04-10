from rest_framework import serializers
from authuser.models import Appointment, AdditionalVisitor, RegularVisitor
from urllib.parse import urljoin
from django.conf import settings


class AdditionalVisitorSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()  # ✅ Convert to full URL
    class Meta:
        model = AdditionalVisitor
        exclude = ['id','participants']

    def get_img(self, obj):
        if obj.img:
            return urljoin(settings.API_BASE_URL, obj.img.url)
        else:
            return 'https://i.pinimg.com/474x/0a/a8/58/0aa8581c2cb0aa948d63ce3ddad90c81.jpg'  # yahaan aap apni default image ka URL daalein



class AppointmentSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SerializerMethodField()
    visitor_img = serializers.SerializerMethodField()  
    additional_visitors = AdditionalVisitorSerializer(many=True, read_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"

    def get_visitor_img(self, obj):
        """Convert visitor_img to full URL"""
        if obj.visitor_img:
            return urljoin(settings.API_BASE_URL, obj.visitor_img.url)
        else:
            return 'https://i.pinimg.com/474x/0a/a8/58/0aa8581c2cb0aa948d63ce3ddad90c81.jpg'  # yahaan aap apni default image ka URL daalein
    
    def get_assigned_to(self, obj):
        """Return assigned user's full name or username"""
        if obj.assigned_to:
            full_name = f"{obj.assigned_to.first_name} {obj.assigned_to.last_name}".strip()
            return full_name if full_name else obj.assigned_to.phone  
        return None
    



class RegularVisitorSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = RegularVisitor
        fields = [
            'id', 'name', 'v_type', 'phone', 'email', 'company_name', 'company_address',
            'image','image', 'created_by', 'updated_by', 'created_at', 'updated_at'
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return urljoin(settings.API_BASE_URL, obj.image.url)
        else:
            return 'https://i.pinimg.com/474x/0a/a8/58/0aa8581c2cb0aa948d63ce3ddad90c81.jpg'  # yahaan aap apni default image ka URL daalein
    
        return None