import json
import uuid
import roborest
from aio_pika import Message
from monitor import get_monitor
from bubblehub.model import RegistrationSpec, MoveSpec
import roborest
from roborest import app


@app.post("/game/{game_id}/player")
async def register_with_game(game_id: str, specs: RegistrationSpec):
    """Register with a game"""
    async with get_monitor():
        player_id = str(uuid.uuid4)
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


@app.put("/game/{game_id}/player/{player_id}")
async def player_move(game_id: str, player_id: str, specs: MoveSpec):
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


@app.get("/game/{game_id}/player/{player_id}")
async def get_status(game_id: str, player_id: str):
    """Get the current player status"""
    result = roborest.status_keeper.get_player(game_id, player_id)
    return result
