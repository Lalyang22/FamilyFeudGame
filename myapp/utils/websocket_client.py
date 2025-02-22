import asyncio
import websockets
import json

WS_SERVER_URL = "ws://localhost:8080"  # WebSocket server URL

async def send_websocket_message(message):
    """Generic function to send a message via WebSocket"""
    try:
        async with websockets.connect(WS_SERVER_URL) as websocket:
            await websocket.send(json.dumps(message))
            print(f"✅ Sent message: {message}")
    except Exception as e:
        print(f"❌ WebSocket Error: {e}")

def send_score_update(team, points):
    """Send score updates to WebSocket"""
    message = {
        "type": "update_score",
        "team": team,
        "points": points
    }
    asyncio.run(send_websocket_message(message))

def send_question(question, answers):
    """Send selected question and possible answers to WebSocket"""
    message = {
        "type": "question_selected",
        "question": question,
        "answers": [answer["text"] for answer in answers],  # Extract text only
        "points": [answer["points"] for answer in answers]  # Extract points only
    }
    asyncio.run(send_websocket_message(message))

def send_answer(answer, pointsToAdd):
    """Send selected answer and points update to WebSocket"""
    message = {
        "type": "answer_selected",
        "answer": answer,
        "pointsToAdd": pointsToAdd
    }
    asyncio.run(send_websocket_message(message))

def send_game_status(winner):
    """Send game status update when the game is finished"""
    message = {
        "type": "game_status",
        "status": "done",
        "winner": winner
    }
    asyncio.run(send_websocket_message(message))
