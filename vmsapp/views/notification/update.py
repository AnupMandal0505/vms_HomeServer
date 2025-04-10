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


class AcceptCall(BaseAuthentication):
    def create(self, request):
        if not request.data.get('id'):
            return Response({'ERR': 'Call id required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            call_notification = CallNotification.objects.get(id=request.data.get('id'))
            call_notification.read = True
            call_notification.save()
            return Response({'success': 'Call marked as read'}, status=status.HTTP_200_OK)
        except CallNotification.DoesNotExist:
            return Response({'ERR': 'Call not found'}, status=status.HTTP_404_NOT_FOUND)
