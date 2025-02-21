from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from myapp.models import FeudQuestion, Game, Round
from .utils.websocket_client import send_score_update, send_question, send_answer, send_game_status


def feud_questions(request):
    """Fetch all questions with their answers in JSON format"""
    questions = FeudQuestion.objects.prefetch_related("answers").all()
    
    data = [
        {
            "question": q.question,
            "answers": [{"text": a.text, "points": a.points} for a in q.answers.all()]
        }
        for q in questions
    ]

    return JsonResponse(data, safe=False)

@csrf_exempt
def save_game(request):
    if request.method == "POST":
        try:
            raw_body = request.body.decode("utf-8")
            print("📥 Raw Request Body:", raw_body)

            data = json.loads(raw_body)
            print("📥 Parsed Data:", json.dumps(data, indent=4))

            required_fields = ["game_name", "game_winner"]
            for field in required_fields:
                if field not in data:
                    return JsonResponse({"error": f"Missing field: {field}"}, status=400)

            game = Game.objects.create(
                game_name=data["game_name"],
                game_winner=data["game_winner"],
                team_1_points=data.get("team_1_points", 0),
                team_2_points=data.get("team_2_points", 0),
                total_rounds=data.get("total_rounds", 3)
            )

            print("✅ Game saved successfully with game_id:", game.game_id)
            return JsonResponse({"message": "Game data saved successfully!", "game_id": game.game_id}, status=201)

        except json.JSONDecodeError:
            print("❌ Error: Invalid JSON format")
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            print(f"❌ Server Error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def save_round(request):
    print("🛠 Endpoint Hit: /api/save-round/")
    
    if request.method == "POST":
        try:
            raw_body = request.body.decode("utf-8")
            print("📥 Raw Request Body:", raw_body)

            data = json.loads(raw_body)
            print("📥 Parsed Data:", json.dumps(data, indent=4))

            if "gameId" not in data:
                return JsonResponse({"error": "Missing 'gameId' in request"}, status=400)

            print(f"🔍 Searching for game with game_id: {data['gameId']}")
            game = Game.objects.filter(game_id=data["gameId"]).first()

            if not game:
                return JsonResponse({"error": "Game not found"}, status=404)

            team1_points = data.get("team1Points", 0)
            team2_points = data.get("team2Points", 0)

            print(f"🔢 Saving Round {data['roundNumber']} - Team 1: {team1_points}, Team 2: {team2_points}")

            new_round = Round.objects.create(
                game=game,
                round_number=data["roundNumber"],
                round_points_team1=team1_points,  
                round_points_team2=team2_points,
                round_winner=data["roundWinner"],
                round_life_team1=data.get("team1Life", 3),
                round_life_team2=data.get("team2Life", 3),
            )

            print(f"✅ Round {new_round.round_number} saved successfully.")

            # ✅ Send score updates via WebSocket
            send_score_update("team1", team1_points)
            send_score_update("team2", team2_points)

            return JsonResponse({"message": "Round saved successfully", "round_id": new_round.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except KeyError as e:
            print(f"❌ Missing key in request: {e}")
            return JsonResponse({"error": f"Missing key: {str(e)}"}, status=400)
        except Exception as e:
            print(f"❌ Server Error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def select_question(request):
    """Send a selected question to WebSocket"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            send_question(data["question"], data["answers"])
            return JsonResponse({"message": "Question sent successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=405)

@csrf_exempt
def select_answer(request):
    """Send selected answer to WebSocket"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            send_answer(data["answer"], data["pointsToAdd"])
            return JsonResponse({"message": "Answer sent successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=405)

@csrf_exempt
def end_game(request):
    """Send game status to WebSocket"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            send_game_status(data["winner"])
            return JsonResponse({"message": "Game status updated successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=405)


def center_view(request):
    return render(request, 'center.html')

def controller_view(request):
    return render(request, 'controller.html')

def landing_view(request):
    return render(request, 'landing.html')

def questions_view(request):
    return render(request, 'questions.html')

def tv_left_view(request):
    return render(request, 'tv-left.html')

def tv_right_view(request):
    return render(request, 'tv-right.html')
