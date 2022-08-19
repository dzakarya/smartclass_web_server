from fastapi import APIRouter
from loguru import logger
from schemas.api_response import ResponseGetValue
from schemas.api_request import TempRequest
from repositories.mqtt import mqtt
from repositories.temp import set_temp, get_temp
router = APIRouter()

@router.get("/get-temp",response_model=ResponseGetValue)
async def gettempvalue():
    value = get_temp()
    return ResponseGetValue(
        data={
            "value":value
        },
        meta=None
    )

@router.post("/set-temp")
async def setlightvalue(req: TempRequest):
    status = set_temp(req.value)
    return{
        "value":status
    }