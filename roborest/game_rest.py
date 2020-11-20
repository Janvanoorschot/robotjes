import json
import uuid
import roborest
from aio_pika import Message
from monitor import get_monitor
from bubblehub.model import RegistrationSpec, CommandSpec
import roborest
from roborest import app


@app.post("/game/{game_id}/player")
async def register_with_game(game_id: str, specs: RegistrationSpec):
    """Register with a game"""
    async with get_monitor():
        player_id = str(uuid.uuid4())
        request = {
            "cmd": "register",
            "game_id": game_id,
            "player_id": player_id,
            "player_name": specs.player_name,
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
        return {
            "player_id": player_id
        }

@app.delete("/game/{game_id}/player/{player_id}")
async def deregister_with_game(game_id: str, player_id: str):
    """Deregister from a game"""
    async with get_monitor():
        request = {
            "cmd": "deregister",
            "game_id": game_id,
            "player_id": player_id,
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
        return {
            "player_id": player_id
        }


@app.get("/game/{game_id}")
async def get_game_status(game_id: str):
    """Get the current game status"""
    result = roborest.status_keeper.get_game_status(game_id)
    return result


@app.get("/game/{game_id}/recording")
async def get_game_status(game_id: str):
    """Get the current game recording"""
    result = roborest.status_keeper.get_game_recording(game_id)
    return result


@app.get("/game/{game_id}/player/{player_id}")
async def get_player_status(game_id: str, player_id: str):
    """Get the current player status"""
    result = roborest.status_keeper.get_player_status(game_id, player_id)
    return result


@app.put("/game/{game_id}/player/{player_id}")
async def player_move(game_id: str, player_id: str, specs: CommandSpec):
    """Move within a game"""
    async with get_monitor():
        request = {
            "cmd": "move",
            "game_id": game_id,
            "player_id": player_id,
            "move": specs.move
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

