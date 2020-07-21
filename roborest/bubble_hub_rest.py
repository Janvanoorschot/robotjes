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
    # async with get_monitor():
    #     request = {
    #         "cmd": "list_games"
    #     }
    #     result = await async_rpc_client.call(request)
    #     return result


@app.get("/games/{game_id}")
async def list_game(game_id: str):
    """Information about a game"""
    async with get_monitor():
        request = {
            "cmd": "get_game",
            "game_id": game_id
        }
        result = await async_rpc_client.call(request)
        return result


@app.put("/games/{game_id}")
async def register_with_game(game_id: str, specs: RegistrationSpec):
    """Register with a game"""
    async with get_monitor():
        request = {
            "cmd": "register",
            "game_id": game_id,
            "player_name": specs.player_name,
            "player_id": specs.player_id,
            "password": specs.game_password
        }
        routing_key = f"{game_id}.game"
        body = json.dumps(request)
        message = Message(
            body.encode(),
            content_type="application/json"
        )
        await roborest.games_exchange.publish(
            message,
            routing_key=routing_key
        )
        return {}


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


