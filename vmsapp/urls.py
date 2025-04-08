from django.urls import path, include
from rest_framework.routers import SimpleRouter
from vmsapp.views import SnacksViewSet, OrderHistoryAPIView,OrderCreateAPIView,OrderUpdate

# Router setup for viewsets
snacks = SimpleRouter()
snacks.register('snacks', SnacksViewSet, basename='snacks')
snacks.register('order', OrderCreateAPIView, basename='order')
snacks.register('order_history', OrderHistoryAPIView, basename='order_history')
snacks.register("update_order_status", OrderUpdate, basename="update_order_status")

urlpatterns = [
    path('appointments/', include('vmsapp.router')),  # Assuming vmsapp/router.py has its own router setup
    path('', include(snacks.urls)),  # include router URLs for viewsets
]
