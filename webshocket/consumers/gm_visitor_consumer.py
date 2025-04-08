import json
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs


class AppointmentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """WebSocket connection starts here"""

        query_string = parse_qs(self.scope["query_string"].decode())  # Extract query params
        self.gm_user_id = query_string.get("gm_user_id", [None])[0]  # Extract gm_user_id
        print("✅ WebSocket Connected for Appointment Updates, User ID:", self.gm_user_id)

        self.room_group_name = "appointments_updates"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print("✅ WebSocket Connected for Appointment Updates")

    async def disconnect(self, close_code):
        """WebSocket disconnect"""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print("❌ WebSocket Disconnected")

    
    async def send_appointment_update(self, event):
        """Send updated appointment data to frontend"""
        data = event["data"]
        if data.get("assigned_to") == self.gm_user_id:  
            # serialized_data = serialize_data(data)  # Convert non-serializable fields
            await self.send(text_data=json.dumps(data))


# def serialize_data(data):
#         """Recursively convert non-serializable data types to JSON-friendly formats."""
#         if isinstance(data, dict):
#             return {k: serialize_data(v) for k, v in data.items()}
#         elif isinstance(data, list):
#             return [serialize_data(v) for v in data]
#         elif isinstance(data, uuid.UUID):  # Convert UUIDs to strings
#             return str(data)
#         return data