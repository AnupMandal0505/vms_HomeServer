
from django.urls import path,include
from vmsapp.views import (AppointmentCreateView,AppointmentForwardGmView,AppointmentListView,AppointmentUpdateView,
                          DeleteAppointmentView,CallVisitorView,RegularVisitorCreate,GetRegularVisitor,GmBussyMode,GetGmBussyMode)
from rest_framework.routers import SimpleRouter

appointment = SimpleRouter()
appointment.register('create-appointments', AppointmentCreateView, basename='create-appointments')
appointment.register('forwards-appointments', AppointmentForwardGmView, basename='forwards-appointments')
appointment.register('regular_visitor_create', RegularVisitorCreate, basename='regular_visitor_create')
appointment.register('get-appointments', AppointmentListView, basename='get-appointments')
appointment.register('get_regular_visitor', GetRegularVisitor, basename='get_regular_visitor')
appointment.register('update-appointments', AppointmentUpdateView, basename='update-appointments')
# appointment.register('unique-visitors', Get_unique_visitor_list, basename='unique-visitors')
appointment.register('delete-appointments', DeleteAppointmentView, basename='delete-appointments')
appointment.register('call-action', CallVisitorView, basename='call-action-visitor')
appointment.register('GmDoNotDisturb', GmBussyMode, basename='GmDoNotDisturb')
appointment.register('get-GmDoNotDisturb', GetGmBussyMode, basename='get-GmDoNotDisturb')



# appointment.register('call', CreateNotification, basename='call')
# appointment.register('contact_list', ContactList, basename='contact_list')
# appointment.register('accept_call', AcceptCall, basename='accept_call')

urlpatterns = appointment.urls
