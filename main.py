from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from pydantic import BaseModel
from repository import save_location

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class Location(BaseModel):
    title: str
    review: str
    long: float
    lat: float

class Msg(BaseModel):
    msg: str


@app.get("/")
async def root():
    return FileResponse('static/add-location.html')

@app.post("/api")
async def root(location: Location):
    print(location)
    id = save_location(location)
    return {"id": 42}

@app.get("/path")
async def demo_get():
    return {"message": "This is /path endpoint, use a post request to transform the text to uppercase"}


@app.post("/path")
async def demo_post(inp: Msg):
    return {"message": inp.msg.upper()}


@app.get("/path/{path_id}")
async def demo_get_path_id(path_id: int):
    return {"message": f"This is /path/{path_id} endpoint, use post request to retrieve result"}