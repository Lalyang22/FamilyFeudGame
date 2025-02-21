from django.urls import re_path
from yourapp.consumers import ScoreConsumer  # Import your WebSocket consumer

websocket_urlpatterns = [
    re_path(r'ws/scores/$', ScoreConsumer.as_asgi()),  # WebSocket path for scores
]
