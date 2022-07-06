from fastapi import APIRouter
from loguru import logger
from ...schemas.api_response import ResponseGetValue
from ...schemas.api_request import LightRequest
router = APIRouter()

@router.get("/get-light-value/",response_model=ResponseGetValue)
async def getlightvalue(zone : int = 0):
    return ResponseGetValue(
        data={
            "value":5
        },
        meta=None
    )

@router.post("/set-light")
async def setlightvalue(req: LightRequest):
    return{
        "zone":req.zone,
        "value":req.value
    }