from fastapi import APIRouter
from loguru import logger

from app.repositories.light import get_light
from ...schemas.api_response import ResponseGetValue
from ...schemas.api_request import LightRequest
router = APIRouter()

@router.get("/get-light",response_model=ResponseGetValue)
async def gettempvalue():
    value = get_light()
    return ResponseGetValue(
        data={
            "value":value
        },
        meta=None
    )

@router.post("/set-light")
async def setlightvalue(req: LightRequest):
    return{
        "zone1":req.zone1,
        "zone2":req.zone2
    }