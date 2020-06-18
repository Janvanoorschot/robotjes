from starlette.responses import RedirectResponse
from pydantic import BaseModel
from roborest import app
from monitor import get_monitor
from bubblehub.model import BubbleStatus, ConnectionSpec, BubbleSpec
from . import async_rpc_client


@app.get("/")
async def redirect():
    response = RedirectResponse(url='/index.html')
    return response


@app.post("/bubbles")
async def create_game(specs: BubbleSpec):
    """ Create a game"""
    async with get_monitor():
        request = {
            "cmd": "create_game",
            "specs": specs.dict()
        }
        result = await async_rpc_client.call(request)
        return result


@app.get("/bubbles")
async def list_games():
    """List current games"""
    async with get_monitor():
        request = {
            "cmd": "list_games"
        }
        result = await async_rpc_client.call(request)
        return result


@app.get("/bubbles/{game_id}")
async def list_game(game_id: str):
    """Information about a game"""
    async with get_monitor():
        request = {
            "cmd": "status_game",
            "game_id": game_id
        }
        result = await async_rpc_client.call(request)
        return result
