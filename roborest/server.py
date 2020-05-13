import uvicorn
from roborest import app
from fastapi.staticfiles import StaticFiles

if __name__ == "__main__":
    app.mount("/", StaticFiles(directory="www"), name="www")
    uvicorn.run(app, host="0.0.0.0", port=8000)
