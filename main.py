from fastapi import FastAPI
from pydantic import BaseModel
import pickle

FILENAME = "plant_data.p"
app = FastAPI()

class PlantStatusData(BaseModel):
    soil_moisture: float = None
    temperature: float = None
    humidity: float = None
    illuminance: float = None


@app.on_event("startup")
async def startup():
    app.state.data = PlantStatusData()
@app.get("/")
async def root():
    # with open(FILENAME, 'rb') as f:
    #     return {"soil_moisture": pickle.load(f),
    #             "temperature": pickle.load(f),
    #             "humidity": pickle.load(f),
    #             "illuminance": pickle.load(f),
    #             }
    return app.state.data


@app.post("/update")
async def update(psd: PlantStatusData):
    app.state.data = psd
    # with open(FILENAME, 'wb') as f:
    #     pickle.dump(psd.soil_moisture, f)
    #     pickle.dump(psd.temperature, f)
    #     pickle.dump(psd.humidity, f)
    #     pickle.dump(psd.illuminance, f)

    return {"success": True, "message": "Data updated"}

@app.get("/update")
async def update():
    # with open(FILENAME, 'rb') as f:
    #     data =  {"soil_moisture": pickle.load(f),
    #             "temperature": pickle.load(f),
    #             "humidity": pickle.load(f),
    #             "illuminance": pickle.load(f),
    #             }
    data = app.state.data

    return {"success": True, "data": data}