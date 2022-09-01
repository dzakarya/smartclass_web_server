from fastapi import APIRouter
from loguru import logger

from repositories.light import get_last_light,set_light,set_automatic,get_mode
from schemas.api_response import ResponseGetLightValue
from schemas.api_request import LightRequest
router = APIRouter()

@router.get("/get-light",response_model=ResponseGetLightValue)
async def gettempvalue():
    value = get_last_light()
    mode = get_mode()
    return ResponseGetLightValue(
        data={
            "zone1":value,
            "zone2":value,
            "mode":mode
        },
        meta=None
    )

@router.post("/set-light")
async def setlightvalue(req: LightRequest):
    result = set_light(req.zone1,req.zone2)
    mode = set_automatic(req.mode)
    return{
        "zone1":req.zone1,
        "zone2":req.zone2,
    }