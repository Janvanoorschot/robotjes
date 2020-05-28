from pydantic import BaseModel

class BubbleSpec(BaseModel):
    size: int
    size: int


class BubbleStatus(BaseModel):
    state: str


class ConnectionSpec(BaseModel):
    size: int

