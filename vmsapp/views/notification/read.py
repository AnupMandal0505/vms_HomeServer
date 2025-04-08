from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from authuser.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from vmsapp.serializers.NotificationSerializer import ContactListSerializer

class BaseAuthentication(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]



class ContactList(BaseAuthentication):
    def list(self, request):
        try:
            # print(request.GET.get("gm_id"))
            data=User.objects.filter(gm=request.GET.get("gm_id"))
            serial=ContactListSerializer(data,many=True)
            return Response({'RES':serial.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Failed to log out'}, status=status.HTTP_400_BAD_REQUEST)
        
