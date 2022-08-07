from fastapi import APIRouter
from loguru import logger
from ...repositories.datalog import get_current_data
from ...schemas.api_request import DatalogRequest
router = APIRouter()

@router.post("/get-data")
async def get_data(req : DatalogRequest):
    get_current_data(req.date, req.time)
    # return ResponseGetValue(
    #     data={
    #         "value":value
    #     },
    #     meta=None
    # )
