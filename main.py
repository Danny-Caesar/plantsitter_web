from fastapi import FastAPI
from pydantic import BaseModel
import os
import pickle

FILENAME = "plant_data.p"
os.chmod(FILENAME, 0o777)
app = FastAPI()

class PlantStatusData(BaseModel):
    soil_moisture: float = None
    temperature: float = None
    humidity: float = None
    illuminance: float = None

@app.get("/")
async def root():
    with open(FILENAME, 'rb') as f:
        return {"soil_moisture": pickle.load(f),
                "temperature": pickle.load(f),
                "humidity": pickle.load(f),
                "illuminance": pickle.load(f),
                }


@app.post("/update")
async def update(psd: PlantStatusData):
    with open(FILENAME, 'wb') as f:
        pickle.dump(psd.soil_moisture, f)
        pickle.dump(psd.temperature, f)
        pickle.dump(psd.humidity, f)
        pickle.dump(psd.illuminance, f)

    return {"success": True, "message": "Data updated"}

@app.get("/update")
async def update():
    with open(FILENAME, 'rb') as f:
        data =  {"soil_moisture": pickle.load(f),
                "temperature": pickle.load(f),
                "humidity": pickle.load(f),
                "illuminance": pickle.load(f),
                }

    return {"success": True, "data": data}