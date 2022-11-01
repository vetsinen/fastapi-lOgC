from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()
client = MongoClient(os.environ['MONGOURL'])

# {
#     name: "Central Park",
#     location: {type: "Point", coordinates: [-73.97, 40.77]},
#     category: "Parks"
# },

def save_location(location):
    db = client.test
    collection = db.locations
    id = collection.insert_one({
        "title": location.title,
        "location": {
            "type": "Point",
            "coordinates":[location.long,  location.lat]
        },
        "review": location.review
    }).inserted_id
    return id

if __name__ == '__main__':
    db = client.test
    collection = db.coll1
    post_id = collection.insert_one({"value":41}).inserted_id
    print(post_id)