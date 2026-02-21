from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv
import certifi

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")
client = AsyncIOMotorClient(
    MONGO_URL,
    tls=True,
    tlsCAFile=certifi.where()
)
# client = AsyncIOMotorClient(MONGO_URL) # Making APi more robust

mongodb_db = client["gen_ai"]
mongodb_collection = mongodb_db["api_testing"]

app = FastAPI()

class MongoDbAPITestingData(BaseModel):
    name: str
    phone: int
    city: str
    course: str

@app.post("/mongodb/insert")
async def mongodb_data_insert_helper(data: MongoDbAPITestingData): 
# async is a not blocking function in a way that other processes will not be disturbed
# await will make sure that it is not blocking any other functiuon, ofr this function it will wait for it's turn
# motor is a driver like pymongo
    reuslt = await mongodb_collection.insert_one(data.dict())
    return {"message":f"Data inserted successfully at {str(reuslt.inserted_id)}"}

def mongodb_get_data_helper(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

@app.get("/mongodb/get_data")
async def get_mongodb_data():
    items = []
    cursor = mongodb_collection.find({})
    async for document in cursor:
        items.append(mongodb_get_data_helper(document))
    return items

# To host this api on cloud, we need to push this code to repo then from repo to cloud so that the api can be accessible to anyone
# Render is a cloud platform, free to use till certain limits
# uvicorn main:app --host 0.0.0.0 --port $PORT
# https://mongodb-api-k4ha.onrender.com -- Render UR