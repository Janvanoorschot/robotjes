import asyncio
from starlette.responses import RedirectResponse
from pydantic import BaseModel
from roborest import app
from . import bubble_rpc_client


class BubbleSpec(BaseModel):
    size: int

class BubbleStatus(BaseModel):
    state: str

class ConnectionSpec(BaseModel):
    size: int

@app.on_event("startup")
async def startup_event():
    await bubble_rpc_client.connect(asyncio.get_running_loop())

@app.get("/")
async def redirect():
    response = RedirectResponse(url='/index.html')
    return response


@app.post("/bubbles")
async def create_bubble(specs: BubbleSpec):
    """ Create a bubble"""
    cmd = {
        "value": "test"
    }
    result = await bubble_rpc_client.call(cmd)
    return result

@app.get("/bubbles")
async def all_bubbles():
    """List current bubbles"""
    return {"message": "all_bubbles"}

@app.get("/bubbles/{bubble_id}")
async def one_bubble(bubble_id: str):
    """Information about a Bubble"""
    return {"message": "one_bubble"}

@app.put("/bubbles/{bubble_id}")
async def one_bubble(state: BubbleStatus):
    """Change state of Bubble"""
    return state

@app.post("/bubbles/{bubble_id}/connections")
async def create_connection(bubble_id: str, specs: ConnectionSpec):
    """Create a connection to a Bubble"""
    return specs

@app.get("/bubbles/{bubble_id}/connections/{connection_id}")
async def one_connection(bubble_id: str, specs: ConnectionSpec):
    """Create a connection to a Bubble"""
    return specs

