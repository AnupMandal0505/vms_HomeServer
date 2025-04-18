# demo/routing.py
from django.urls import re_path

from .consumers import appointment_consumers,call_consumer,canteen_consumer,gm_visitor_consumer,pa_visitor_consumer

websocket_urlpatterns = [
    re_path('ws/appointment/$', appointment_consumers.IndexPageConsumer.as_asgi()),

    re_path('ws/call/(?P<user_id>[0-9a-fA-F-]+)/$',call_consumer.CallLiveConsumer.as_asgi()),

    re_path('ws/snacks/$', canteen_consumer.OrderLiveConsumer.as_asgi()),
    
    re_path('ws/gm_visitors/$', gm_visitor_consumer.AppointmentConsumer.as_asgi()),
    re_path('ws/pa_visitors/$', pa_visitor_consumer.AppointmentConsumer.as_asgi()),

]

