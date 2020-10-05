import json
from aio_pika import IncomingMessage, Message, ExchangeType
from starlette.responses import RedirectResponse
from pydantic import BaseModel
import roborest
from roborest import app
from monitor import get_monitor
from bubblehub.model import GameSpec, RegistrationSpec
from . import async_rpc_client, games_exchange_name, channel


@app.get("/")
async def redirect():
    response = RedirectResponse(url='/index.html')
    return response


@app.post("/games")
async def create_game(specs: GameSpec):
    """ Create a game"""
    async with get_monitor():
        request = {
            "cmd": "create_game",
            "specs": specs.dict()
        }
        result = await async_rpc_client.call(request)
        return result


@app.get("/games")
async def list_games():
    """List current games"""
    lst = roborest.status_keeper.list_games()
    return lst


@app.get("/mazes")
async def list_mazes():
    """List current mazes"""
    async with get_monitor():
        request = {
            "cmd": "list_mazes"
        }
        result = await async_rpc_client.call(request)
        return result


@app.get("/mazes/{maze_id}")
async def list_maze(maze_id: str):
    """List specific maze"""
    async with get_monitor():
        request = {
            "cmd": "get_maze",
            "maze_id": maze_id
        }
        result = await async_rpc_client.call(request)
        return result


