
from django.urls import path,include
from vmsapp.views import (AppointmentCreateView,AppointmentListView,AppointmentUpdateView,DeleteAppointmentView,
                          OrderCreateAPIView,OrderHistoryAPIView,OrderUpdate,CreateNotification,ContactList,AcceptCall,CallVisitorView,Get_unique_visitor_list)
from rest_framework.routers import SimpleRouter

appointment = SimpleRouter()
appointment.register('create-appointments', AppointmentCreateView, basename='create-appointments')
appointment.register('get-appointments', AppointmentListView, basename='get-appointments')
appointment.register('update-appointments', AppointmentUpdateView, basename='update-appointments')
appointment.register('unique-visitors', Get_unique_visitor_list, basename='unique-visitors')
appointment.register('delete-appointments', DeleteAppointmentView, basename='delete-appointments')
appointment.register('call-action', CallVisitorView, basename='call-action-visitor')


# appointment.register('snacks', SnacksViewSet, basename='snacks')
# appointment.register('order', OrderCreateAPIView, basename='order')
# appointment.register('order_history', OrderHistoryAPIView, basename='order_history')
# appointment.register("update_order_status", OrderUpdate, basename="update_order_status")

appointment.register('call', CreateNotification, basename='call')
appointment.register('contact_list', ContactList, basename='contact_list')
appointment.register('accept_call', AcceptCall, basename='accept_call')

urlpatterns = appointment.urls
