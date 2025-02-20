from django.shortcuts import render
from myapp import views


def landing_page(request):
    return render(request, 'landing.html')
