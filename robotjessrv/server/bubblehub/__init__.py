from enum import Enum


class GameStatus(Enum):
    IDLE = 'idle'
    CREATED = 'created'
    GAMETICK = 'gametick'
    DELTAREC = 'deltarec'
    STARTED = 'started'
    STOPPED = 'stopped'


from robotjes.server import Player, RoboGame, Field
from .bubble import Bubble
from .bubble_hub import BubbleHub


