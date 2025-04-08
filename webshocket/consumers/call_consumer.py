from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging

logger = logging.getLogger(__name__)

class CallLiveConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(65654654)
        """Connect WebSocket and add to group."""
        self.receive_id = self.scope['url_route']['kwargs']['user_id']
        print(self.receive_id)
        await self.accept()
        await self.channel_layer.group_add('call_live', self.channel_name)
        logger.info(f"✅ WebSocket {self.channel_name} connected and added to group.")

    async def disconnect(self, close_code):
        """Disconnect WebSocket and remove from group."""
        await self.channel_layer.group_discard('call_live', self.channel_name)
        logger.warning(f"❌ WebSocket {self.channel_name} disconnected with code {close_code}")

    async def call_notify(self, event):
        """Handle call_notify message type."""
        data = event['data']
        logger.info(f"📞 Call Notification Sent: {data}")

        # Convert UUID objects to strings (Avoid JSON errors)
        data['sender'] = str(data['sender'])
        data['receiver'] = str(data['receiver'])
        if data['receiver']!=self.receive_id:
            return

        await self.send(text_data=json.dumps({
            'type': 'call_notify',
            'data': data
        }))
