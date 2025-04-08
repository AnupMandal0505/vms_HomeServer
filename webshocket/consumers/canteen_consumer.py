from channels.generic.websocket import AsyncWebsocketConsumer
import json

class OrderLiveConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Connect WebSocket and add to group."""
        await self.accept()
        await self.channel_layer.group_add('order_live', self.channel_name)

    async def disconnect(self, close_code):
        """Disconnect WebSocket and remove from group."""
        await self.channel_layer.group_discard('order_live', self.channel_name)
        
    async def order_notify(self, event):
        """Handle order_notify message type."""
        data = event['data']
        # print("sad",data)

        # Send JSON response
        await self.send(text_data=json.dumps({
                'type': 'order_notify',
                'data': data}))