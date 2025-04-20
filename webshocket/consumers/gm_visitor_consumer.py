import json
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs

import logging

logger = logging.getLogger(__name__)

class AppointmentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """WebSocket connection starts here"""

        query_string = parse_qs(self.scope["query_string"].decode())  # Extract query params
        self.user_id = query_string.get("user_id", [None])[0]  # Extract gm_user_id
        self.role = query_string.get("role", [None])[0]  # Extract role
        logger.info(f"🚀 WebSocket connected: user_id={self.user_id}, role={self.role}")

        # print(" WebSocket Connected for Appointment Updates, User ID:", self.gm_user_id)

        self.room_group_name = "appointments_updates"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        # print(" WebSocket Connected for Appointment Updates")

    async def disconnect(self, close_code):
        """WebSocket disconnect"""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        # print(" WebSocket Disconnected")

    
    async def send_appointment_update(self, event):
        """Send updated appointment data to frontend"""
        data = event["data"]
        if "gm" == self.role:
            if data.get("gm") == self.user_id:  
                # serialized_data = serialize_data(data)  # Convert non-serializable fields
                await self.send(text_data=json.dumps(data))
        elif "secretary" == self.role:
            if data.get("assigned_to") == self.user_id:  
                await self.send(text_data=json.dumps(data))
        else:
            if data.get("created_by") == self.user_id:  
                await self.send(text_data=json.dumps(data))