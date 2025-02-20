from django.urls import path
from myapp import views  # Replace 'myapp' with your actual app name

urlpatterns = [
    path('center/', views.center_view, name='center'),
    path('controller/', views.controller_view, name='controller'),
    path('landing/', views.landing_view, name='landing'),
    path('questions/', views.questions_view, name='questions'),
    path('tv-left/', views.tv_left_view, name='tv-left'),
    path('tv-right/', views.tv_right_view, name='tv-right'),
    path('api/feud/', views.feud_questions, name='feud_questions'),
]
