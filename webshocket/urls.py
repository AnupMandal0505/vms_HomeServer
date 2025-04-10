from rest_framework.routers import SimpleRouter
# from authuser.views import CallGenerate, AcceptCall, ContactList, SnacksViewSet,ActiveDisplay,DeActiveDisplay,OrderHistoryAPIView,OrderCreateAPIView,CheckUserViewSet,UpdateOrderStatus
from vmsapp.views.notification.create import CreateNotification
from vmsapp.views.notification.read import ContactList
from vmsapp.views.notification.update import AcceptCall

# from vmsapp.views.notification.create import CreateNotification
# from vmsapp.views.notification.read import ContactList
# from vmsapp.views.notification.update import AcceptCall

api_router = SimpleRouter()
# api_router.register('call', CreateNotification, basename='call')
# api_router.register('contact_list', ContactList, basename='contact_list')
# api_router.register('accept_call', AcceptCall, basename='accept_call')
# api_router.register('snacks', SnacksViewSet, basename='snacks')
# api_router.register('order', OrderCreateAPIView, basename='order')
# api_router.register('order_history', OrderHistoryAPIView, basename='order_history')
# api_router.register('check-user',CheckUserViewSet, basename='check_user')
# api_router.register("update_order_status", UpdateOrderStatus, basename="update_order_status")
# api_router.register("activate_display", ActiveDisplay, basename="activate_display_urls")
# api_router.register("deactivate_display", DeActiveDisplay, basename="deactivate_display_urls")

urlpatterns = api_router.urls