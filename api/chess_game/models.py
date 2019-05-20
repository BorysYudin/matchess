from django.contrib.auth.models import User
from django.db import models


class Games(models.Model):
    uuid = models.UUIDField()
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                   related_name='created_by')
    white_pieces_player = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                            related_name='white_pieces_player',
                                            null=True)
    black_pieces_player = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                            related_name='black_pieces_player',
                                            null=True)
    is_started = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
