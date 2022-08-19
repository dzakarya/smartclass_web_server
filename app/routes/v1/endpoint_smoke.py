from fastapi import APIRouter
from loguru import logger
from schemas.api_response import ResponseGetValue
from repositories.mqtt import mqtt
from repositories.smoke import get_smoke
router = APIRouter()

@router.get("/get-smoke",response_model=ResponseGetValue)
async def get_smoke_status():
    value = get_smoke()
    return ResponseGetValue(
        data={
            "value":value
        },
        meta=None
    )
