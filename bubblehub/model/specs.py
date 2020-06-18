from typing import List
from pydantic import BaseModel

class BubbleSpec(BaseModel):
    size: int
    size: int


class BubbleStatus(BaseModel):
    state: str


class ConnectionSpec(BaseModel):
    size: int


class PlayerStatus(BaseModel):
    id: str


class GameStatus(BaseModel):
    id: str
    players: List[PlayerStatus]


