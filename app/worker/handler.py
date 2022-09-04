
from worker.people_detector import PeopleDetector
from loguru import logger
import threading
from config.constant import lowest_light_value,highest_light_value
from repositories.light import set_light
from repositories.temp import set_temp
from repositories.mqtt import mqtt

class BackgroundTasks(threading.Thread):
    
    def __init__(self,) -> None:
        super(BackgroundTasks,self).__init__()
        self.detector_thread = PeopleDetector("rtsp://admin:Poltekpelsorong1@192.168.0.50:554/Streaming/channels/102/")
        self.detector_thread.start()
        self.detector_thread2 = PeopleDetector("rtsp://admin:Poltekpelsorong1@192.168.0.50:554/Streaming/channels/302/")
        self.detector_thread2.start()
        self.isDark = False

    def run(self,*args,**kwargs):
        while True:
            if mqtt.isautomatic:
                if mqtt.startCounter:
                    self.detector_thread.reset_counter()
                    self.detector_thread2.reset_counter()
                    logger.info("Counter is reset ")
                    mqtt.startCounter = False

                if self.detector_thread.setLightOff and self.detector_thread2.setLightOff:
                    if mqtt.get_last_light() > lowest_light_value:
                        mqtt.light = lowest_light_value
                        set_light(lowest_light_value,lowest_light_value)
                        set_temp(0)
                        
                else:
                    if mqtt.get_last_light() < highest_light_value and self.isDark==True:
                        mqtt.light = highest_light_value 
                        set_light(highest_light_value,highest_light_value)
                        set_temp(20)
                        self.isDark = False

                #condition when user set dark with automatic mode want to turn all the light without counter

                if self.detector_thread.people_num != 0 or self.detector_thread2.people_num != 0:
                    logger.info("people detected")
                    if mqtt.get_last_light() < highest_light_value:
                        mqtt.light = highest_light_value 
                        set_light(highest_light_value,highest_light_value)
                        set_temp(20)