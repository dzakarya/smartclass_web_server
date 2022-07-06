from fastapi import APIRouter
from loguru import logger
from ...schemas.api_response import ResponseGetValue
from ...schemas.api_request import TempRequest
router = APIRouter()

@router.get("/get-temp",response_model=ResponseGetValue)
async def gettempvalue():
    return ResponseGetValue(
        data={
            "value":5
        },
        meta=None
    )

@router.post("/set-light")
async def setlightvalue(req: TempRequest):
    return{
        "zone":req.zone,
        "value":req.value
    }