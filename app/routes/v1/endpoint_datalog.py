from fastapi import APIRouter
from loguru import logger
from repositories.datalog import get_current_data
from schemas.api_request import DatalogRequest
from schemas.api_response import ResponseGetDataLog
router = APIRouter()

@router.post("/get-data")
async def get_data(req : DatalogRequest):
    result = get_current_data(req.date, req.time)
    return ResponseGetDataLog(
        data=result,
        meta=None
    )
