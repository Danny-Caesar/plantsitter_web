from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PlantStatusData(BaseModel):
    soil_moisture: float = None
    temperature: float = None
    humidity: float = None
    illuminance: float = None

data =  PlantStatusData()

@app.get("/")
async def root():
    if data is None:
        return {"message": "No data updated"}

    return {"soil_moisture": data.soil_moisture,
            "temperature": data.temperature,
            "humidity": data.humidity,
            "illuminance": data.illuminance}

@app.post("/update")
async def update(psd: PlantStatusData):
    data.soil_moisture = psd.soil_moisture
    data.temperature = psd.temperature
    data.humidity = psd.humidity
    data.illuminance = psd.illuminance

    return {"success": True, "message": "Data updated"}

@app.get("/update")
async def update():
    if data is None:
        return {"success": False, "message": "No data updated"}

    return {"success": True, "data": data}