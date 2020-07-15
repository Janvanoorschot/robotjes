import asyncio
from fastapi_utils.tasks import repeat_every
import roborest
from roborest import app, pikaurl
from monitor import mon
from aio_pika import connect, ExchangeType
import config
from . import async_rpc_client, games_exchange_name, async_topic_listener



@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_running_loop()
    roborest.connection = await connect(roborest.pikaurl, loop=loop)
    roborest.channel = await roborest.connection.channel()
    roborest.games_exchange = await roborest.channel.declare_exchange(games_exchange_name, ExchangeType.TOPIC)
    await mon.connect(loop, roborest.channel)
    await async_rpc_client.connect(loop, roborest.channel)
    await async_topic_listener.connect(loop, roborest.channel)


@app.on_event("startup")
@repeat_every(seconds=2)
async def timer_task():
    await mon.timer()

