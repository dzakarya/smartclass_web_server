import sched
import time
from ..model.light_handler import LightHandler
from ..model.smoke_handler import SmokeHandler
from ..model.temp_handler import TempHandler
from ..repositories.mqtt import mqtt
from loguru import logger

s = sched.scheduler(time.time, time.sleep)


def light_thread():
    LHandler = LightHandler()
    LHandler.insert_light_once(mqtt.light)

def smoke_thread():
    SHandler = SmokeHandler()
    SHandler.insert_smoke_once(mqtt.smoke)

def temp_thread():
    THandler = TempHandler()
    THandler.insert_temp_once(mqtt.temp) 

def thread_event(sc): 
    try:
        light_thread()
    except Exception as e:
        logger.error(e)
    try:
        smoke_thread()
    except Exception as e:
        logger.error(e)
    try:
        temp_thread()
    except Exception as e:
        logger.error(e)

    sc.enter(5, 1, thread_event, (sc,))

def start_scheduler():
    s.enter(5, 1, thread_event, (s,))
    s.run()