from fastapi import APIRouter
from loguru import logger

from app.repositories.light import LightRepository
from ...schemas.api_response import ResponseGetLightValue
from ...schemas.api_request import LightRequest
router = APIRouter()

@router.get("/get-light",response_model=ResponseGetLightValue)
async def gettempvalue():
    Lrep = LightRepository()
    Lrep.get_light()
    return ResponseGetLightValue(
        data={
            "zone1":0,
            "zone2":0
        },
        meta=None
    )

@router.post("/set-light")
async def setlightvalue(req: LightRequest):
    Lrep = LightRepository()
    Lrep.set_light(req.zone1)
    return{
        "zone1":req.zone1,
        "zone2":req.zone2
    }