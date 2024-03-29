from fastapi import APIRouter
from .v1 import endpoint_light,endpoint_temp,endpoint_smoke,endpoint_datalog

api_router = APIRouter()

api_router.include_router(endpoint_light.router, tags=['light'], prefix='/light')
api_router.include_router(endpoint_temp.router, tags=['temp'], prefix='/temp')
api_router.include_router(endpoint_smoke.router, tags=['smoke'],prefix='/smoke')
api_router.include_router(endpoint_datalog.router, tags=['data'], prefix='/data')
