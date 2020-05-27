from starlette.responses import RedirectResponse
from pydantic import BaseModel
from roborest import app
from monitor import get_monitor
from . import async_rpc_client


class BubbleSpec(BaseModel):
    size: int
    size: int


class BubbleStatus(BaseModel):
    state: str


class ConnectionSpec(BaseModel):
    size: int

@app.get("/")
async def redirect():
    response = RedirectResponse(url='/index.html')
    return response


@app.post("/bubbles")
async def create_bubble(specs: BubbleSpec):
    """ Create a bubble"""
    async with get_monitor():
        cmd = {
            "value": "create_bubble"
        }
        result = await async_rpc_client.call(cmd)
        return result


@app.get("/bubbles")
async def list_all_bubbles():
    """List current bubbles"""
    async with get_monitor():
        cmd = {
            "value": "list_all_bubbles"
        }
        result = await async_rpc_client.call(cmd)
        return result


@app.get("/bubbles/{bubble_id}")
async def list_one_bubble(bubble_id: str):
    """Information about a Bubble"""
    async with get_monitor():
        cmd = {
            "value": "list_one_bubble"
        }
        result = await async_rpc_client.call(cmd)
        return result


@app.put("/bubbles/{bubble_id}")
async def change_bubble(state: BubbleStatus):
    """Change state of Bubble"""
    async with get_monitor():
        cmd = {
            "value": "change_bubble"
        }
        result = await async_rpc_client.call(cmd)
        return result


@app.post("/bubbles/{bubble_id}/connections")
async def create_connection(bubble_id: str, specs: ConnectionSpec):
    """Create a connection to a Bubble"""
    async with get_monitor():
        cmd = {
            "value": "create_connection"
        }
        result = await async_rpc_client.call(cmd)
        return result


@app.get("/bubbles/{bubble_id}/connections/{connection_id}")
async def list_one_connection(bubble_id: str, specs: ConnectionSpec):
    """Create a connection to a Bubble"""
    async with get_monitor():
        cmd = {
            "value": "list_one_connection"
        }
        result = await async_rpc_client.call(cmd)
        return result

