import os
import sys
from asyncio import Queue
import traceback
from . import app, templates, rootdir, websockets


from fastapi import Request, status, WebSocket
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse, FileResponse

from fastapi_utils.tasks import repeat_every

@app.on_event("startup")
async def startup_event():
    pass

@app.on_event("startup")
@repeat_every(seconds=2)
async def timer_task():
    for sessionid, queue in websockets.items():
        await queue.put(f"eikel")

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


@app.get("/favicon.ico", response_class=HTMLResponse)
async def root(request: Request):
    return FileResponse(os.path.join(rootdir, "www.mon/img/favicon.ico"))


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return RedirectResponse("/bmon")


@app.get("/bmon", response_class=HTMLResponse)
async def root(request: Request):
    if 'i' in request.session:
        request.session['i'] = request.session['i'] + 1
    else:
        request.session['i'] = 0
    return templates.TemplateResponse("main.html", {"request": request, "i": request.session['i']})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    if 'session' in websocket.cookies:
        queue = Queue()
        sessionid = websocket.cookies['session']
        websockets[sessionid] = queue
        while True:
            msg = await queue.get()
            await websocket.send_text(msg)




