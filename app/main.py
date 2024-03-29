from multiprocessing.managers import Server
from threading import Thread
from fastapi import FastAPI
from loguru import logger
from routes import index, api
import threading
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette import status
from config.constant import lowest_light_value,highest_light_value
from schemas.http_response import HTTPResponseWrapper,ErrorMessage

from core.json import Jsonify

from repositories.mqtt import mqtt
from worker.db_scheduler import start_scheduler
from worker.people_detector import PeopleDetector
import uvicorn
from repositories.light import set_light
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

class BackgroundTasks(threading.Thread):
    def __init__(self,) -> None:
        super(BackgroundTasks,self).__init__()
        self.detector_thread = PeopleDetector("rtsp://admin:Poltekpelsorong1@192.168.0.8:554/Streaming/channels/2/")
        self.detector_thread.start()
        self.detector_thread2 = PeopleDetector("rtsp://admin:Poltekpelsorong1@192.168.0.5:554/Streaming/channels/2/")
        self.detector_thread2.start()
        self.isDark = False
    def run(self,*args,**kwargs):
        while True:
            if self.detector_thread.setLightOff and self.detector_thread2.setLightOff:
                if mqtt.get_last_light() > lowest_light_value:
                    mqtt.light = lowest_light_value
                    set_light(lowest_light_value,lowest_light_value)
                    self.isDark = True
            else:
                if mqtt.get_last_light() < highest_light_value and self.isDark==True:
                    mqtt.light = highest_light_value 
                    set_light(highest_light_value,highest_light_value)
                    self.isDark = False
            

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
