from fastapi import APIRouter
from loguru import logger

from repositories.light import get_light,set_light
from schemas.api_response import ResponseGetLightValue
from schemas.api_request import LightRequest
router = APIRouter()

@router.get("/get-light",response_model=ResponseGetLightValue)
async def gettempvalue():
    value = get_light()
    return ResponseGetLightValue(
        data={
            "zone1":value,
            "zone2":value
        },
        meta=None
    )

@router.post("/set-light")
async def setlightvalue(req: LightRequest):
    result = set_light(req.zone1,req.zone2)
    return{
        "zone1":req.zone1,
        "zone2":req.zone2
    }