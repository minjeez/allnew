from fastapi import FastAPI 
from pydantic.main import BaseModel
import getFoodData as gF
import getRCPData as gRCP

app = FastAPI()

@app.get('/')
async def healthCheck():
    return "OK"

@app.get('/food')
async def getFood():
    return gF.NewData()[0]