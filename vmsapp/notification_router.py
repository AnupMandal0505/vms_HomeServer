
from django.urls import path,include
from vmsapp.views import (CreateNotification,ContactList,AcceptCall,CallVisitorView)
from rest_framework.routers import SimpleRouter

notification = SimpleRouter()
notification.register('call-action', CallVisitorView, basename='call-action-visitor')
notification.register('call', CreateNotification, basename='call')
notification.register('contact_list', ContactList, basename='contact_list')
notification.register('accept_call', AcceptCall, basename='accept_call')

urlpatterns = notification.urls
