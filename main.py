from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

import repository #import save_location,get_all_locations, get_last_locations

from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

class Location(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    title: str
    review: str
    long: float
    lat: float

class Msg(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    msg: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

@app.get("/")
async def index():
    return FileResponse('static/add-location.html')

@app.get("/locations")
async def map():
    return FileResponse('static/locations.html')

@app.get("/map")
async def map():
    return FileResponse('static/map.html')

@app.post("/api")
async def location(location: Location):
    print(location)
    id = repository.save_location(location)
    return {"status": 200}

@app.get("/api/all")
async def location():
    return repository.get_all_locations()

@app.get("/api/last")
async def last_location():
    return repository.get_last_locations()

@app.delete("/api/{id}")
async def delete(id:str):
    repository.remove(id)
    return {"v":id}

@app.get("/path")
async def demo_get():
    return {"message": "This is /path endpoint, use a post request to transform the text to uppercase"}


@app.post("/path")
async def demo_post(inp: Msg):
    return {"message": inp.msg.upper()}


@app.get("/path/{path_id}")
async def demo_get_path_id(path_id: int):
    return {"message": f"This is /path/{path_id} endpoint, use post request to retrieve result"}