import sys
import traceback
import datetime
import asyncio

from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from fastapi_utils.tasks import repeat_every
from .. import roborest
from robotjessrv.server.roborest import app
from robotjessrv.server.monitor import mon
from aio_pika import connect, ExchangeType
from . import async_rpc_client, games_exchange_name, field_exchange_name, async_topic_listener, async_field_listener



@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_running_loop()
    roborest.connection = await connect(roborest.pikaurl, loop=loop)
    roborest.channel = await roborest.connection.channel()
    roborest.games_exchange = await roborest.channel.declare_exchange(games_exchange_name, ExchangeType.TOPIC)
    roborest.field_exchange = await roborest.channel.declare_exchange(field_exchange_name, ExchangeType.FANOUT)
    await mon.connect(loop, roborest.channel)
    await async_rpc_client.connect(loop, roborest.channel)
    await async_topic_listener.connect(loop, roborest.channel)
    await async_field_listener.connect(loop, roborest.channel)


@app.on_event("startup")
@repeat_every(seconds=2)
async def timer_task():
    now = datetime.datetime.now()
    await mon.timer(now)
    roborest.status_keeper.timer(now)

@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    # this handles incaught exceptions in the server code.
    # send information to the client for development purposes (only in development mode?)
    exc_type, value, exc_traceback = sys.exc_info()
    resp = JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({
            "msg": str(exc),
            "exception": str(exc_type),
            "stack": traceback.format_exception(exc)
        })
    )
    return resp

