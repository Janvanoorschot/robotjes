from enum import Enum


class GameStatus(Enum):
    IDLE = 'idle'
    CREATED = 'created'
    UPDATE  = 'update'
    STARTED = 'started'
    STOPPED = 'stopped'


from .game import Game
from .player import Player
from .bubble import Bubble
from .bubble_hub import BubbleHub


