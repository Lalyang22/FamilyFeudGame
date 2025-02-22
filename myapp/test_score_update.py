import asyncio
import websockets
import json

async def send_score_update(team, points):
    async with websockets.connect("ws://localhost:8080") as websocket:
        message = json.dumps({
            "type": "update_score",
            "team": team,
            "points": points
        })
        await websocket.send(message)
        print(f"✅ Sent {points} points to {team}")

# Update scores manually
asyncio.run(send_score_update("team1", 50))  # Add 50 points to Team 1
asyncio.run(send_score_update("team2", 100))  # Add 100 points to Team 2
