from django.urls import path
from myapp import views  # Replace 'myapp' with your actual app name

urlpatterns = [
    path('center/', views.center_view, name='center'),
    path('center-fast-money/', views.center_fast_money_view, name='center-fast-money'),
    path('controller/', views.controller_view, name='controller'),
    path('landing/', views.landing_view, name='landing'),
    path('questions/', views.questions_view, name='questions'),
    path('tv-left/', views.tv_left_view, name='tv-left'),
    path('tv-right/', views.tv_right_view, name='tv-right'),
    path('fastmoney-admin/', views.fastmoney_admin, name='fastmoney-admin'),

    # API
    path('api/feud/', views.get_questions, name="get_questions"),  # ✅ Use this for fetching game questions
    path('api/flag-question/<int:question_id>/', views.flag_question, name="flag_question"),  # ✅ Flag a used question
    path('api/reset_flags/', views.reset_flags, name='reset_flags'),
    path("api/save-game/", views.save_game, name="save_game"),
    path("api/save-round/", views.save_round, name="save_round"),
    # Fast Money
    path("api/fastmoney_questions/", views.fast_money_questions, name="fast_money_questions"),
    path("api/flag_fastmoney/<int:question_id>/", views.flag_fastmoney_question, name="flag_fastmoney_question"),
    path("api/reset_fastmoney/", views.reset_fastmoney_flags, name="reset_fastmoney_flags"),

]
