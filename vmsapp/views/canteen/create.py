from rest_framework import viewsets, status
from rest_framework.response import Response
from authuser.models import Order,OrderItem
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from django.db import transaction  #  Import this at top

class BaseAuthentication(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]



class OrderCreateAPIView(BaseAuthentication):
    def create(self, request):
        print(request.data)
        with transaction.atomic():
            try:
                order = Order.objects.create(created_by=request.user)

                order_items = []
                order_data = request.data.get("order_data", {})

                for category, items in order_data.items():
                    for item in items:
                        order_items.append(OrderItem(
                            order=order,
                            order_type=category,  # ✅ Here you add WATER / FOOD etc.
                            order_item=item["name"],
                            qty=item["quantity"]
                        ))

                OrderItem.objects.bulk_create(order_items)

                return Response({"RES": True}, status=status.HTTP_201_CREATED)

            except Exception as e:
                print("Error:", e)
                return Response({"RES": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




# class CheckUserViewSet(viewsets.ViewSet):
#     def create(self, request):
#         screen_id = request.data.get("screen_id")
#         password = request.data.get("password")

#         if not screen_id or not password:
#             return Response({"ERR": "Screen ID and password are required"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             screen_activity = ScreenActivity.objects.get(screen_id=screen_id)

#             if check_password(password, screen_activity.password):
#                 screen_activity.is_active=True
#                 screen_activity.save()
#                 display_user = screen_activity.live_user
#                 return Response({
#                     "RES": [
#                         {
#                             "screen_id":screen_activity.screen_id,
#                             "live_fetch_id": display_user.id,
#                             "phone": display_user.email,  # Assuming email is used as phone
#                             "name": display_user.phone
#                         }
#                     ]
#                 }, status=status.HTTP_200_OK)
#             else:
#                 return Response({"ERR": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)

#         except ScreenActivity.DoesNotExist:
#             return Response({"ERR": "Screen ID not found"}, status=status.HTTP_404_NOT_FOUND)

