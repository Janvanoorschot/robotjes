import json
from aio_pika import Message
from monitor import get_monitor
from bubblehub.model import RegistrationSpec, MoveSpec
import roborest
from roborest import app


@app.put("/game/{game_id}/register")
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


@app.put("/game/{game_id}/move")
async def player_move(game_id: str, specs: MoveSpec):
    """Move within a game"""
    async with get_monitor():
        request = {
            "cmd": "move",
            "player_id": specs.player_id,
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
