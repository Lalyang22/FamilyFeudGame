from django.urls import path
from myapp import views  # Replace 'myapp' with your actual app name

def debug_urls():
    print("📢 URLs Loaded!")
    for pattern in urlpatterns:
        print(f"🔹 {pattern}")

urlpatterns = [
    path('center/', views.center_view, name='center'),
    path('controller/', views.controller_view, name='controller'),
    path('landing/', views.landing_view, name='landing'),
    path('questions/', views.questions_view, name='questions'),
    path('tv-left/', views.tv_left_view, name='tv-left'),
    path('tv-right/', views.tv_right_view, name='tv-right'),

    # API
    path('api/feud/', views.feud_questions, name='feud_questions'),
    path("api/save-game/", views.save_game, name="save_game"),
    path("api/save-round/", views.save_round, name="save_round"),


]

debug_urls()  # ✅ Add this to check if Django is loading your URLs