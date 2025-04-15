from rest_framework import viewsets, status
from rest_framework.response import Response
from authuser.models import User
from authuser.models import Order,OrderItem
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from vmsapp.serializers.CanteenSerializer import SnacksSerializer,OrderSerializer
from django.utils.timezone import localtime

class BaseAuthentication(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]



# class OrderUpdate(BaseAuthentication):
#     def list(self, request):
#         try:
#             order_up=Order.objects.filter(id=request.GET.get("id"))
#             order_up.updated_by=request.user
#             order_up.status=True
#             order_up.save()
#             return Response({"RES":True},status=status.HTTP_200_OK)
#         except Exception as e:

#             return Response({"ERR":False},status=status.HTTP_400_BAD_REQUEST)

class OrderUpdate(viewsets.ViewSet):
    def list(self, request):
        try:
            order_id = request.GET.get("id")  # Use request.data for POST, PUT, PATCH
            if not order_id:
                return Response({"ERR": "Missing 'id' parameter"}, status=status.HTTP_400_BAD_REQUEST)

            order = Order.objects.get(id=order_id)
            order.status = True  # Update the status
            order.save()

            return Response({"RES": True}, status=status.HTTP_200_OK)

        except Order.DoesNotExist:
            return Response({"ERR": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"ERR": str(e)}, status=status.HTTP_400_BAD_REQUEST)
