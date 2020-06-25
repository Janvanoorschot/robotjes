from typing import List
from pydantic import BaseModel

class GameSpec(BaseModel):
    name: str
    password: str
    maze_id: str


class PlayerState(BaseModel):
    id: str

class GameState(BaseModel):
    id: str
    status: str
    players: List[PlayerState]


