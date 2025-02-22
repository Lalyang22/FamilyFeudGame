import asyncio
import websockets
import json
import time  

clients = {}  # Track connected clients
team_scores = {"team1": 0, "team2": 0}  # Store scores
last_scores = {"team1": 0, "team2": 0}  # Store last confirmed score
game_status = "playing"


async def handle_client(websocket, path=None):
    """Handles WebSocket connections"""
    try:
        async for message in websocket:
            data = json.loads(message)

            if data["type"] == "register":
                client_id = data["clientId"]

                # ✅ Allow only specific client IDs
                allowed_clients = ["admin", "center", "questions", "monitor_team1", "monitor_team2"]
                if client_id not in allowed_clients:
                    print(f"⚠️ Unrecognized client ID: {client_id} (Ignoring)")
                    return
                
                clients[client_id] = websocket  # ✅ Store WebSocket with predefined names
                print(f"✅ {client_id} registered successfully.")

                # ✅ Send current scores after successful registration
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

            elif data["type"] == "game_status":
                global game_status  # ✅ Declare as global BEFORE modifying
                game_status = "done"  # ✅ Now Python knows it's a global variable
                
                winner = data["winner"]
                print(f"🏆 Game finished. Winner: {winner}")

                await broadcast_to_clients({
                    "type": "game_status",
                    "status": "done",
                    "winner": winner
                })

            elif data["type"] == "question_selected":
                game_status = "done"  # ✅ Now safe to modify

                # Extract only text and points separately
                question_payload = {
                    "type": "question_selected",
                    "question": data["question"],
                    "answers": [answer["text"] for answer in data["answers"]],  # Extract text
                    "points": [answer["points"] for answer in data["answers"]]  # Extract points
                }

                # Send to Questions Viewer
                if "questions" in clients:
                    await clients["questions"].send(json.dumps({
                        "type": "question_selected",
                        "question": data["question"]
                    }))
                    print(f"📤 Sent question to questions: {data['question']}")

                # Send to Center
                if "center" in clients:
                    await clients["center"].send(json.dumps(question_payload))
                    print(f"📤 Sent question to center: {data['question']}")

            elif data["type"] == "answer_selected":
                answer_text = data["answer"]
                pointsToAdd = data["pointsToAdd"]

                # If game is finished, stop counting points but still reveal the answer
                if game_status == "done":
                    pointsToAdd = 0  # Stop adding points but still flip answers

                print(f"🎯 Answer Selected: {answer_text} (Points Added: {pointsToAdd})")

                # Broadcast to Center
                if "center" in clients:
                    await clients["center"].send(json.dumps({
                        "type": "answer_selected",
                        "answer": answer_text,
                        "pointsToAdd": pointsToAdd  # Send 0 if game is done
                    }))

    except websockets.exceptions.ConnectionClosed:
        print(f"❌ Client disconnected.")
    finally:
        await remove_disconnected_clients(websocket)

async def remove_disconnected_clients(websocket):
    """Remove a disconnected client from the client list."""
    disconnected_clients = [client_id for client_id, ws in clients.items() if ws == websocket]
    
    for client_id in disconnected_clients:
        del clients[client_id]
        print(f"🔴 Removed disconnected client: {client_id}")

async def broadcast_scores():
    """Broadcast the updated scores to all clients."""
    score_message = json.dumps({
        "type": "score_update",
        "team1": team_scores["team1"],
        "team2": team_scores["team2"]
    })

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
