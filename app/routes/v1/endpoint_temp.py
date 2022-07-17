from fastapi import APIRouter
from loguru import logger
from ...schemas.api_response import ResponseGetValue
from ...schemas.api_request import TempRequest
from ...repositories.mqtt import mqtt
router = APIRouter()

@router.get("/get-temp",response_model=ResponseGetValue)
async def gettempvalue():
    return ResponseGetValue(
        data={
            "value":mqtt.temp
        },
        meta=None
    )

@router.post("/set-light")
async def setlightvalue(req: TempRequest):
    return{
        "zone":req.zone,
        "value":req.value
    }