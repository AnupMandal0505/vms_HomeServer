from rest_framework import serializers
from authuser.models import Appointment,AdditionalVisitor,GMTraffic
from urllib.parse import urljoin
from django.conf import settings
from urllib.parse import urljoin
from django.conf import settings


class DisplayAppointmentSerializer(serializers.ModelSerializer):
    id = serializers.CharField()  # Appointment ID as string
    assigned_to = serializers.CharField(source='assigned_to_id', allow_null=True)  # FK ID as string, nullable
    created_by = serializers.CharField(source='created_by_id', allow_null=True)  # FK ID as string, nullable
    assign_name = serializers.SerializerMethodField()  # ✅ To get assigned GM name
    # company_display_name = serializers.SerializerMethodField()  # ✅ Custom field for company or visitor name

    class Meta:
        model = Appointment
        fields = [
            'id', 
            'assigned_to', 
            'assign_name', 
            'company_name',
            'visitor_name',
            'status',
            'created_by', 
            'created_at'
        ]


    def get_assign_name(self, obj):
        if obj.gm:
            # logger.debug(f"GM: {obj.gm.first_name}")
            return f"{obj.gm.first_name} {obj.gm.last_name}"

        elif obj.assigned_to:
            return f"{obj.assigned_to.first_name} {obj.assigned_to.last_name}"
        else:
            return None
   



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
    assign_name = serializers.SerializerMethodField()  # ✅ To get assigned GM name

    class Meta:
        model = Appointment
        fields = "__all__"

    def get_assign_name(self, obj):
        if obj.gm:
            # logger.debug(f"GM: {obj.gm.first_name}")
            return f"{obj.gm.first_name} {obj.gm.last_name}"

        elif obj.assigned_to:
            return f"{obj.assigned_to.first_name} {obj.assigned_to.last_name}"
        else:
            return None

    def get_visitor_img(self, obj):
        """Convert visitor_img to full URL"""
        if obj.visitor_img:
            return urljoin(settings.API_BASE_URL, obj.visitor_img.url)
        else:
            return 'https://i.pinimg.com/474x/0a/a8/58/0aa8581c2cb0aa948d63ce3ddad90c81.jpg'  # yahaan aap apni default image ka URL daalein
    



from django.utils import timezone
from datetime import date

class GmTrafficSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['id', 'gm', 'status']

    def get_status(self, obj):
        # today = timezone.now().date()
        today = date.today()

        # Check if GM is assigned
        if not obj.gm:
            return "available"

        # Check GMTraffic for that GM
        gm_traffic = GMTraffic.objects.filter(gm=obj.gm).first()
        if gm_traffic and gm_traffic.status:
            return "busy"

        # Check if there's any progress appointment for today with same GM
        has_progress = Appointment.objects.filter(
            gm=obj.gm,
            date=today,
            status__iexact="progress"
        ).exclude(id=obj.id).exists()

        if has_progress:
            return "progress"

        return "available"