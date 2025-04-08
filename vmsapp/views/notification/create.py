from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from authuser.models import CallNotification
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from vmsapp.serializers.NotificationSerializer import CallNotificationSerializer,ContactListSerializer


class BaseAuthentication(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]


# API View for creating a notification
class CreateNotification(BaseAuthentication):
    def create(self, request):
        try:
            CallNotification.objects.create(receiver=request.user,sender=request.data.get("sender_id"))
            return Response({"RES": True })
        except Exception as e:
            return Response({"ERR": False })

