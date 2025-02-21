import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ScoreConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handle new WebSocket connection"""
        await self.accept()
        print("🔗 WebSocket connected")

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        print("❌ WebSocket disconnected")

    async def receive(self, text_data):
        """Handle incoming messages"""
        data = json.loads(text_data)
        team = data.get("team")
        points = data.get("points")

        print(f"📥 Received Score Update: {team} -> {points} points")

        # Broadcast the score update to all WebSocket clients
        await self.send(text_data=json.dumps({
            "type": "update_score",
            "team": team,
            "points": points,
        }))
