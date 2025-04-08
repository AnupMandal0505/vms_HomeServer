from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio  # Added for periodic ping
from asgiref.sync import sync_to_async
from authuser.models import Appointment
from datetime import date
from authuser.models import User
from webshocket.serializers.live_appoint_serializers import DisplayAppointmentSerializer

class IndexPageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Connect WebSocket and add to group."""
        await self.accept()
        await self.channel_layer.group_add('index_page', self.channel_name)
        print(f"✅ WebSocket {self.channel_name} added to group: index_page")

        # Initialize filters
        self.filter_date = date.today().strftime('%Y-%m-%d')
        self.filter_created_by_id = None
        self.filter_role = None

        # Start heartbeat (ping) to keep connection alive
        self.ping_task = asyncio.create_task(self.heartbeat())

    async def receive(self, text_data):
        """Receive filter parameters from frontend."""
        data = json.loads(text_data)

        # Store filter parameters from frontend
        self.filter_date = data.get("date", date.today().strftime("%Y-%m-%d"))  
        self.filter_created_by_id = data.get("created_by_id", None)
        self.filter_role = data.get("role", "assigned_to")  

        # Validate user
        try:
            self.user = await sync_to_async(User.objects.get)(id=self.filter_created_by_id)
        except User.DoesNotExist:
            await self.send(text_data=json.dumps({"error": "User not found"}))
            return

        # Fetch filtered data asynchronously
        initial_data = await self.get_posts(self.filter_date, self.user, self.filter_role)

        # Send JSON response
        await self.send(text_data=json.dumps({
            'type': 'initial_data',
            'data': initial_data,
        }))

    async def disconnect(self, close_code):
        """Disconnect WebSocket and remove from group."""
        print(f"❌ WebSocket {self.channel_name} disconnected with code: {close_code}")
        await self.channel_layer.group_discard('index_page', self.channel_name)

        # Cancel the ping task to stop sending heartbeat messages
        if hasattr(self, "ping_task"):
            self.ping_task.cancel()

    async def update_index_page(self, event):
        """Send real-time updates to WebSocket clients, but only if relevant."""
        updated_data = event.get('data', {})

        is_relevant = (
            (updated_data.get("assigned_to") == str(self.user.id)) or
            (updated_data.get("created_by") == str(self.user.id))
        )

        print("update",is_relevant)
        # Send JSON response only if relevant
        # if is_relevant:
        await self.send(text_data=json.dumps({
            'type': 'update_index_page',
            'data': updated_data
        }))

    @sync_to_async
    def get_posts(self, filter_date, user, role):
        """Fetch appointments based on filters."""
        try:
            filter_date = date.fromisoformat(filter_date)  
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD."}

        # Fix: Use filter_date instead of self.filter_date
        if role == "assigned_to":
            posts = Appointment.objects.filter(date=filter_date, assigned_to=user)
        else:
            posts = Appointment.objects.filter(date=filter_date, created_by=user)
        return DisplayAppointmentSerializer(posts, many=True).data 

    async def heartbeat(self):
        """Periodically send ping messages to keep WebSocket alive."""
        while True:
            await asyncio.sleep(30)  # Every 30 seconds
            try:
                await self.send(json.dumps({"type": "ping"}))
            except:
                break  # Stop loop if WebSocket is closed
