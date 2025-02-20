from django.shortcuts import render
from django.http import JsonResponse
from myapp.models import FeudQuestion

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
