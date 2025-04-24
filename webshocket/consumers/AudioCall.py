import json
from urllib.parse import parse_qs
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from asgiref.sync import sync_to_async

class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = AnonymousUser()
        query = parse_qs(self.scope["query_string"].decode())
        token_key = query.get("token", [None])[0]

        if token_key:
            try:
                token = await sync_to_async(Token.objects.get)(key=token_key)
                self.user = await sync_to_async(lambda: token.user)()
            except Token.DoesNotExist:
                pass

        if not self.user or self.user.is_anonymous:
            await self.close()
            return

        self.room_name = str(self.user.id)
        self.room_group_name = f"call_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        target_user_id = data.get("target")
        data["sender"] = str(self.user.id)  # Include sender ID

        if target_user_id:
            await self.channel_layer.group_send(
                f"call_{target_user_id}",  # 👈 Forward to target's group
                {
                    "type": "send.sdp",
                    "data": data
                }
            )



    async def send_sdp(self, event):
        await self.send(text_data=json.dumps(event["data"]))
