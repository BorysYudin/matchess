from uuid import uuid4

from django.core.cache import cache

from channels.generic.websocket import JsonWebsocketConsumer

from .models import Games
from engine.models import Game


class ChessGameConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def receive_json(self, content, **kwargs):
        command = content.get("command", None)

        if command == 'create':
            self.create_game()

    def create_game(self):
        uuid = uuid4()
        game = Games.objects.create(uuid=uuid, created_by=self.scope['user'],
                                    white_pieces_player=self.scope['user'])
        game_object = Game()
        cache.set(uuid, game_object)
        pass
