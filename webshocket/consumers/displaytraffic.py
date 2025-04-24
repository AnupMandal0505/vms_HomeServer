# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

import logging
# Get the logger instance
logger = logging.getLogger(__name__)  #


class AppointmentStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        gm_id = self.scope['url_route']['kwargs']['gm_id']
        self.group_name = f'gm_{gm_id}'
        logger.info(f'Successful operation1: {self.group_name} ✅')

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def appointment_status_update(self, event):
        data = event['data']
        # await self.send(text_data=json.dumps(data))
        event_gm_id = data.get('gm_id')
        current_gm_id = self.group_name.replace('gm_', '')

        # Match only if gm_id matches the current consumer
        if event_gm_id == current_gm_id:
            await self.send(text_data=json.dumps(data))
