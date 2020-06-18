from typing import List
from pydantic import BaseModel

class BubbleSpec(BaseModel):
    size: int
    size: int


class BubbleStatus(BaseModel):
    state: str


class ConnectionSpec(BaseModel):
    size: int


class PlayerState(BaseModel):
    id: str


class GameState(BaseModel):
    id: str
    status: str
    players: List[PlayerState]


