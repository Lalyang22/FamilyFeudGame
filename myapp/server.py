import asyncio
import websockets
import json
import time  

clients = {}  # Track connected clients
game_status = "playing"  # Track game state
team_scores = {"team1": 0, "team2": 0}  # Store scores
last_scores = {"team1": 0, "team2": 0}  # Store last confirmed score

async def handle_client(websocket, path=None):
    """Handles WebSocket connections"""
    try:
        async for message in websocket:
            data = json.loads(message)

            if data["type"] == "register":
                client_id = data["clientId"]
                clients[client_id] = websocket
                print(f"✅ {client_id} registered successfully.")

                # ✅ Send current scores to newly connected clients
                await websocket.send(json.dumps({
                    "type": "score_update",
                    "team1": team_scores["team1"],
                    "team2": team_scores["team2"]
                }))

            elif data["type"] == "update_score":
                team = data.get("team")
                new_score = data.get("points", 0)  # Treat `points` as the new score, not an addition

                # Prevent invalid updates
                if team not in team_scores or not isinstance(new_score, int):
                    print(f"⚠️ Invalid update: {data}")
                    return

                # Prevent duplicate updates
                if team_scores[team] == new_score:
                    print(f"⚠️ Duplicate score update ignored for {team}: {new_score}")
                    return

                print(f"🛠️ Updating {team} score: {new_score} (Before: {team_scores[team]})")
                
                team_scores[team] = new_score  # ✅ Overwrite instead of adding
                last_scores[team] = new_score  # ✅ Store last confirmed score
                print(f"✅ {team} new score: {team_scores[team]}")

                await broadcast_scores()

            elif data["type"] == "reset_scores":
                team_scores["team1"] = 0
                team_scores["team2"] = 0
                last_scores["team1"] = 0
                last_scores["team2"] = 0
                print("🔄 Scores manually reset!")

                await broadcast_scores()

            elif data["type"] == "start_new_game":
                team_scores["team1"] = 0
                team_scores["team2"] = 0
                last_scores["team1"] = 0
                last_scores["team2"] = 0
                print("🔄 Scores reset for new game!")

                await broadcast_scores()

            elif data["type"] == "game_status":
                global game_status
                game_status = "done"
                winner = data["winner"]
                print(f"🏆 Game finished. Winner: {winner}")

                await broadcast_to_clients({
                    "type": "game_status",
                    "status": "done",
                    "winner": winner
                })

    except websockets.exceptions.ConnectionClosed:
        print(f"❌ Client disconnected.")
    finally:
        await remove_disconnected_clients(websocket)

async def broadcast_scores():
    """Broadcast the updated scores to all clients."""
    score_message = json.dumps({
        "type": "score_update",
        "team1": team_scores["team1"],
        "team2": team_scores["team2"]
    })

    await broadcast_to_clients(score_message)

async def broadcast_scores():
    """Broadcast the updated scores to all clients."""
    score_message = json.dumps({
        "type": "score_update",
        "team1": team_scores["team1"],
        "team2": team_scores["team2"]
    })

    print(f"📡 Broadcasting Score Update: {score_message}")

    await broadcast_to_clients(score_message)


async def broadcast_to_clients(message):
    """Send a message to all connected clients and log their IDs."""
    disconnected_clients = []
    
    for client_id, ws in clients.items():
        try:
            await ws.send(message)
            print(f"📤 Sent to {client_id}: {message}")
        except websockets.exceptions.ConnectionClosed:
            disconnected_clients.append(client_id)

    for client_id in disconnected_clients:
        del clients[client_id]
        print(f"🔴 Removed disconnected client: {client_id}")
async def main():
    """Start the WebSocket server"""
    print("🚀 WebSocket Server Started on ws://localhost:8080")
    async with websockets.serve(handle_client, "localhost", 8080):
        await asyncio.Future()  

try:
    asyncio.run(main())
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
