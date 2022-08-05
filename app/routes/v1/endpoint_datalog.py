from fastapi import APIRouter
from loguru import logger
from ...schemas.api_request import DatalogRequest
router = APIRouter()

@router.post("/get-data")
async def get_data(req : DatalogRequest):
    logger.info(req.date)
    logger.info(req.time)
    # return ResponseGetValue(
    #     data={
    #         "value":value
    #     },
    #     meta=None
    # )
