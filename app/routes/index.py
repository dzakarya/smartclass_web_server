
from ..core.json import Jsonify
from fastapi import APIRouter
from ..schemas.http_response import HTTPResponseWrapper
router = APIRouter()
@router.get("/healthzx",
            description="health check",
            status_code=200)
async def healthzx():
    return Jsonify(
        content=HTTPResponseWrapper(
            error=False,
            meta={
                "message": "I am healthy"
            }
        ),
        status_code=200
    )
