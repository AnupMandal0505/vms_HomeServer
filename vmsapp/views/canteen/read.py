from rest_framework import viewsets, status
from rest_framework.response import Response
from authuser.models import Order,Snacks
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from vmsapp.serializers.CanteenSerializer import SnacksSerializer,OrderSerializer
from django.utils.timezone import localtime

class BaseAuthentication(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]

# Snacks ViewSet
class SnacksViewSet(viewsets.ReadOnlyModelViewSet):  # Only GET methods allowed
    queryset = Snacks.objects.all()
    serializer_class = SnacksSerializer


class OrderHistoryAPIView(viewsets.ViewSet):
    def list(self, request):
        serial=OrderSerializer(Order.objects.filter(created_at__date= localtime().date()), many=True)
        return Response({"RES":True,"data":serial.data})

