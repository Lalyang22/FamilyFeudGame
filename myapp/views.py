from django.shortcuts import render

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
