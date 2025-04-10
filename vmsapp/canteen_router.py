
from django.urls import path,include
from vmsapp.views import SnacksViewSet, OrderHistoryAPIView,OrderCreateAPIView,OrderUpdate

from rest_framework.routers import SimpleRouter

# Router setup for viewsets
canteen = SimpleRouter()
canteen.register('snacks', SnacksViewSet, basename='snacks')
canteen.register('order', OrderCreateAPIView, basename='order')
canteen.register('order_history', OrderHistoryAPIView, basename='order_history')
canteen.register("update_order_status", OrderUpdate, basename="update_order_status")

urlpatterns = canteen.urls
