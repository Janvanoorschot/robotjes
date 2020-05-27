import asyncio
from fastapi_utils.tasks import repeat_every
import roborest
from roborest import app, pikaurl
from monitor import mon
from aio_pika import connect
from . import async_rpc_client



@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_running_loop()
    roborest.connection = await connect(roborest.pikaurl, loop=loop)
    roborest.channel = await roborest.connection.channel()
    await mon.connect(loop, roborest.channel)
    await async_rpc_client.connect(loop, roborest.channel)


@app.on_event("startup")
@repeat_every(seconds=2)
async def timer_task():
    await mon.timer()

