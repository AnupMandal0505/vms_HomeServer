from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from authuser.models import Appointment
from webshocket.serializers.live_appoint_serializers import DisplayAppointmentSerializer,AppointmentSerializer
from authuser.models import CallNotification,Order
from webshocket.serializers.call_serializers import CallNotificationSerializer
from webshocket.serializers.canteen_serializers import GetOrderSerializer
from django.utils.timezone import now



@receiver(post_save, sender=Appointment)
def update_index_page(sender, instance, **kwargs):
    """Send only relevant updates to WebSocket group"""
    channel_layer = get_channel_layer()

    # Serialize the updated appointment
    serializer = DisplayAppointmentSerializer(instance)
    serialized_data = serialize_data(serializer.data)  # Convert UUIDs to string

    # Send the updated appointment data to the WebSocket group
    async_to_sync(channel_layer.group_send)(
    'index_page',  
    {
        'type': 'update_index_page',  # Must match exactly
        'data': serialized_data
    }
    
    )







@receiver(post_save, sender=CallNotification)
def call_notify(sender, instance, **kwargs):
    """Send only relevant updates (Today's & Pending) to WebSocket group"""
    channel_layer = get_channel_layer()
    
    # Check if the instance is today's and has status 'pending'
    if instance.read == False:
        # Serialize the filtered instance
        serialized_data = CallNotificationSerializer(instance).data
        async_to_sync(channel_layer.group_send)(
            'call_live',  
            {
                'type': 'call_notify',
                'data': serialized_data  # Sending only filtered data
            }
        )




@receiver(post_save, sender=Order)
def order_notify(sender, instance, **kwargs):
    """Send only relevant updates (Today's & Pending) to WebSocket group"""
    channel_layer = get_channel_layer()
    
    # Check if the instance is today's and has status 'pending'
    if instance.status == False and instance.created_at.date() == now().date():
        # Serialize the filtered instance
        serialized_data = GetOrderSerializer(instance).data

        async_to_sync(channel_layer.group_send)(
            'order_live',  
            {
                'type': 'order_notify',
                'data': serialized_data  # Sending only filtered data
            }
        )




# gm visitor list live......................
@receiver(post_save, sender=Appointment)
def send_appointment_update(sender, instance, **kwargs):
    """Send update only when an appointment is modified"""
    channel_layer = get_channel_layer()
    serializer = AppointmentSerializer(instance)

    serialized_data = serialize_data(serializer.data)  # Convert UUIDs to string
    # print(serialized_data)
    async_to_sync(channel_layer.group_send)(
        "appointments_updates",
        {
            "type": "send_appointment_update",
            "data": serialized_data,  # Now using properly serialized data
        },
    )


import uuid

def serialize_data(data):
    """Recursively convert non-serializable data types to JSON-friendly formats."""
    if isinstance(data, dict):
        return {k: serialize_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [serialize_data(v) for v in data]
    elif isinstance(data, uuid.UUID):  # Convert UUIDs to strings
        return str(data)
    return data
