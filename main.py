from fastapi import FastAPI
from pydantic import BaseModel
import os
import ssl
from dotenv import load_dotenv

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

KEYFILE = "key.pem"
CRTFILE = "crt.pem"
key = os.environ["SERVER_KEY"]
crt = os.environ["SERVER_CRT"]

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

class PlantStatusData(BaseModel):
    soil_moisture: float = None
    temperature: float = None
    humidity: float = None
    illuminance: float = None


@app.on_event("startup")
async def startup():
    app.state.data = PlantStatusData()

    with open(KEYFILE, "w") as f:
        f.write(key)
        f.close()

    with open(CRTFILE, "w") as f:
        f.write(crt)
        f.close()

    context.load_cert_chain(certfile=CRTFILE, keyfile=KEYFILE)

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