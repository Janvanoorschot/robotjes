from enum import Enum


class GameStatus(Enum):
    IDLE = 'idle'
    CREATED = 'created'
    GAMETICK = 'gametick'
    DELTAREC = 'deltarec'
    STARTED = 'started'
    STOPPED = 'stopped'

from .player import Player
from .robo_game import RoboGame
from .game import Game
from .field import Field
from .bubble import Bubble
from .bubble_hub import BubbleHub


