import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime
from bson.json_util import dumps
from bson.json_util import loads
from bson.objectid import ObjectId

load_dotenv()
client = MongoClient(os.environ['MONGOURL'])
db = client.test
collection = db.locations

# {
#     name: "Central Park",
#     location: {type: "Point", coordinates: [-73.97, 40.77]},
#     category: "Parks"
# },
def save_location(location):
    id = collection.insert_one({
        "title": location.title,
        "location": {
            "type": "Point",
            "coordinates":[location.long,  location.lat]
        },
        "review": location.review,
        "creation": datetime.now(),
    }).inserted_id
    return id

def get_last_locations():
    #TODO: use pydantic serializer
    cursor = collection.find({}, {'_id': 1, 'title':1, 'review':1})\
        .sort([("creation", pymongo.DESCENDING)]).limit(3)
    docs =  loads(dumps(cursor))

    rez = []
    for loc in docs:
        print(type(loc), str(loc['_id']))
        rez.append({
            "id": str(loc['_id']),
            "title": loc['title'],
            "review": loc['review'][0:15]
        })
    return rez

def get_all_locations():
    # TODO: use pydantic serializer
    cursor = collection.find({}, {'_id': 1, 'title': 1, 'review': 1})
    docs = loads(dumps(cursor))

    rez = []
    for loc in docs:
        rez.append({
            "id": str(loc['_id']),
            "title": loc['title'],
            "review": loc['review']
        })
    return rez

def remove(id:str):
    print(type(id), id)
    collection.delete_one({'_id': ObjectId(id)})

if __name__ == '__main__':
    db = client.test
    collection = db.coll1
    post_id = collection.insert_one({"value":41}).inserted_id
    print(post_id)