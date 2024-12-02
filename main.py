from fastapi import FastAPI
from pydantic import BaseModel

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
    return app.state.data


@app.post("/update")
async def update(psd: PlantStatusData):
    app.state.data = psd

    return {"success": True, "message": "Data updated"}

@app.get("/update")
async def update():
    data = app.state.data

    return {"success": True, "data": data}