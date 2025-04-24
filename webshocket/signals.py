from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from authuser.models import Appointment,GMTraffic
from webshocket.serializers.live_appoint_serializers import DisplayAppointmentSerializer,AppointmentSerializer,GmTrafficSerializer
from authuser.models import CallNotification,Order
from webshocket.serializers.call_serializers import CallNotificationSerializer
from webshocket.serializers.canteen_serializers import GetOrderSerializer
from django.utils.timezone import now

channel_layer = get_channel_layer()


# @receiver(post_save, sender=GMTraffic)
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



from django.db import transaction

@receiver(post_save, sender=Order)
def order_notify(sender, instance, **kwargs):
    """Queue the notification to happen after the transaction completes"""
    transaction.on_commit(lambda: send_order_notification(instance))

def send_order_notification(order_instance):
    """Send only relevant updates (Today's & Pending) to WebSocket group"""
    channel_layer = get_channel_layer()
    
    # Check if the instance is today's and has status 'pending'
    if order_instance.status == False and order_instance.created_at.date() == now().date():
        # Serialize the filtered instance - now with OrderItems properly associated
        serialized_data = GetOrderSerializer(order_instance).data

        async_to_sync(channel_layer.group_send)(
            'order_live',  
            {
                'type': 'order_notify',
                'data': serialized_data
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





# AudioCalll..................
# from pyfcm import FCMNotification

# def send_push_notification(token, title, body):
#     push_service = FCMNotification(api_key='aebed3b20d156d31e4a1abafcaa4ab944b4138e5')
#     result = push_service.notify_single_device(
#         registration_id=token,
#         message_title=title,
#         message_body=body
#     )
#     return result

# @receiver(post_save, sender=Appointment)
# def send_update(sender, instance, **kwargs):
#     # Only send the update if the status has changed or appointment is created or deleted
#     channel_layer = get_channel_layer()

#     # Prepare the data to send, ensure you convert UUID to string
#     data = {
#         # 'id': str(instance.id),
#         'status': instance.status,  # Assuming 'status' is part of the Appointment model
#         'gm_id': str(instance.gm.id) if instance.gm else None,  # gm_id as string
#     }

#     # Broadcast the status update to the appropriate group
#     async_to_sync(channel_layer.group_send)(
#         f'gm_{instance.gm.id}',  # Group based on gm_id
#         {
#             'type': 'appointment_status_update',
#             'data': data,
#         }
#     )

from django.utils import timezone
import logging
from datetime import date
# Get the logger instance
logger = logging.getLogger(__name__)  # Use the current module name

@receiver(post_save, sender=GMTraffic)
@receiver(post_save, sender=Appointment)
def send_update(sender, instance, **kwargs):
    # Only send the update if the status has changed or appointment is created or deleted
    channel_layer = get_channel_layer()

    # Get today's date for the serializer
    # today = timezone.now().date()
    today = date.today()

    # Serialize the Appointment data along with the status logic
    gm_traffic = GMTraffic.objects.filter(gm=instance.gm).first() if instance.gm else None
    if instance.gm:
        # Here, we are using the custom logic from your GmTrafficSerializer
        traffic_data = {
            'id': str(instance.id),
            'gm': str(instance.gm.id),  # Assuming gm is a ForeignKey to the GM model
            'status': 'available',  # Default status
        }

        # Check if GM is assigned and compute the status
        if not instance.gm:
            traffic_data['status'] = "available"
        elif gm_traffic and gm_traffic.status:
            traffic_data['status'] = "busy"
        else:
            has_progress = Appointment.objects.filter(
                gm=instance.gm,
                date=today,
                status="progress"
            ).exists()
            logger.info(f'Successful operation: {has_progress} ✅')

            if has_progress:
                traffic_data['status'] = "progress"
            else:
                traffic_data['status'] = "available"

    # Prepare the data to send to WebSocket client
    data = {
        'status': traffic_data['status'],
        'gm_id': traffic_data['gm'],  # gm_id as string
    }

    # Broadcast the status update to the appropriate group
    if instance.gm:
        async_to_sync(channel_layer.group_send)(
            f'gm_{instance.gm.id}',  # Group based on gm_id
            {
                'type': 'appointment_status_update',
                'data': data,
            }
        )