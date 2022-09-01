from threading import Thread

from fastapi import FastAPI

from loguru import logger

from routes import index, api

from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette import status

from schemas.http_response import HTTPResponseWrapper,ErrorMessage

from core.json import Jsonify

import uvicorn
from repositories.mqtt import mqtt

from worker.db_scheduler import start_scheduler
from worker.handler import BackgroundTasks

log = logger
def create_http_server() -> FastAPI:
    """Create HTTP Server instance to hold the endpoints"""
    kwargs = {
        "title": "SmartClass",
        "version": "1.0.0",
        "debug": "true",
        "openapi_url": f"/api/v1/openapi.json",
        'docs_url': '/ainARycO',
        'redoc_url': '/ainARycOm'
    }

    log.info("initializing http server...")

    server = FastAPI(**kwargs)
    return server

def attach_exception_handler(server: FastAPI) -> FastAPI:
    @server.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request, exc):
        return Jsonify(content=HTTPResponseWrapper(
            error=True,
            data=None,
            meta=ErrorMessage(message=str(exc.detail), type="external")
        ), status_code=exc.status_code)

    @server.exception_handler(Exception)
    async def handle_unexpected_exception(request: Request, exc: Exception):
        log.exception(f"got critical error: {exc} when performing request: {request.method.upper()} {request.url}",
                      exc_info=False)
        return Jsonify(content=HTTPResponseWrapper(
            error=True,
            data=None,
            meta=ErrorMessage(message=f"internal server error, {exc}", type="internal")
        ), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return server

def configure_http_server(server: FastAPI) -> FastAPI:

    log.info("initializing http server...")
   
    server.include_router(index.router)
    server.include_router(api.api_router)
    log.info("adding sauce(s) to http server...")
    server = attach_exception_handler(server)    
    return server



app = configure_http_server(create_http_server())
            

@app.on_event("startup")
async def startup_event():
    thread = Thread(target=start_scheduler)
    thread.start()
    t = BackgroundTasks()
    t.start()

if __name__ == "__main__":
    mqtt.mqtt_client.loop_start()
    uvicorn.run(app, host="0.0.0.0", port=8080)
    
    # thread = Thread(target=start_scheduler)
    # thread.start()
    # detector_thread = PeopleDetector(0)
    # detector_thread.run()
