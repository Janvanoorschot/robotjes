from starlette.responses import RedirectResponse
from .. import roborest
from . import app
from robotjessrv.server.monitor import get_monitor
from robotjessrv.server.bubblehub.model import GameSpec
from . import async_rpc_client

import uuid
import json
from aio_pika import Message

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

@app.post("/confirm/{uid}")
async def confirm_with_game(uid: str):
    """Confirm registration  with a game using a UUID"""
    async with get_monitor():
        specs = roborest.status_keeper.get_reservation(uid)
        if specs:
            player_id = specs["player_id"]
            game_id = specs["game_id"]
            player_name = specs["player_name"]
            password = specs["password"]
            request = {
                "cmd": "register",
                "game_id": game_id,
                "player_id": player_id,
                "player_name": player_name,
                "password": password
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
            roborest.status_keeper.update_reservation(uid, "confirmed")
            return {
                "player_id": player_id,
                "game_id": game_id
            }
        else:
            raise Exception(f"unknown uuid {uid}")


@app.get("/info/{uid}")
async def info_about_game(uid: str):
    """Get information about a game given a UUID"""
    async with get_monitor():
        specs = roborest.status_keeper.get_reservation(uid)
        if specs:
            player_id = specs["player_id"]
            game_id = specs["game_id"]
            status = "running"
            return {
                "status": status,
                "player_id": player_id,
                "game_id": game_id
            }
        else:
            return {
                "status": "unknown"
            }
