from django.urls import path

from . import consumers


websocket_urlpatterns = [
    path('ws/chess_game/', consumers.ChessGameConsumer),
]
