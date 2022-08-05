from fastapi import APIRouter
from loguru import logger
from ...schemas.api_request import DatalogRequest
router = APIRouter()

@router.post("/get-data")
async def get_smoke_status(req):
    logger.info(req)
    # return ResponseGetValue(
    #     data={
    #         "value":value
    #     },
    #     meta=None
    # )
