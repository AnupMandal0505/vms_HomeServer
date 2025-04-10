from rest_framework import serializers
from authuser.models import Appointment,AdditionalVisitor
from urllib.parse import urljoin
from django.conf import settings
from urllib.parse import urljoin
from django.conf import settings


class DisplayAppointmentSerializer(serializers.ModelSerializer):
    id = serializers.CharField()  # Appointment ID as string
    assigned_to = serializers.CharField(source='assigned_to_id', allow_null=True)  # FK ID as string, nullable
    created_by = serializers.CharField(source='created_by_id', allow_null=True)  # FK ID as string, nullable
    gm_name = serializers.SerializerMethodField()  # ✅ To get assigned GM name
    # company_display_name = serializers.SerializerMethodField()  # ✅ Custom field for company or visitor name

    class Meta:
        model = Appointment
        fields = [
            'id', 
            'assigned_to', 
            'gm_name', 
            'company_name',
            'visitor_name',
            'status',
            'created_by', 
            'created_at'
        ]

    def get_gm_name(self, obj):
        return obj.assigned_to.first_name if obj.assigned_to else None

   



class AdditionalVisitorSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()  # ✅ Convert to full URL
    # img = serializers.ImageField(required=False, allow_null=True)  # ✅ Fix: Allows None
    class Meta:
        model = AdditionalVisitor
        exclude = ['id','participants']

    def get_img(self, obj):
        if obj.img:
            return urljoin(settings.API_BASE_URL, obj.img.url)
        else:
            return 'https://i.pinimg.com/474x/0a/a8/58/0aa8581c2cb0aa948d63ce3ddad90c81.jpg'  # yahaan aap apni default image ka URL daalein



class AppointmentSerializer(serializers.ModelSerializer):
    visitor_img = serializers.SerializerMethodField()  # ✅ Convert to full URL
    additional_visitors = AdditionalVisitorSerializer(many=True, read_only=True)
    # visitor_img = serializers.ImageField(required=False, allow_null=True)  # ✅ Fix: Allows file upload

    class Meta:
        model = Appointment
        fields = "__all__"

    def get_visitor_img(self, obj):
        """Convert visitor_img to full URL"""
        if obj.visitor_img:
            return urljoin(settings.API_BASE_URL, obj.visitor_img.url)
        else:
            return 'https://i.pinimg.com/474x/0a/a8/58/0aa8581c2cb0aa948d63ce3ddad90c81.jpg'  # yahaan aap apni default image ka URL daalein
    
