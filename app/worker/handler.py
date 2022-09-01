
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
        self.detector_thread = PeopleDetector("rtsp://admin:Poltekpelsorong1@192.168.0.8:554/Streaming/channels/2/")
        self.detector_thread.start()
        self.detector_thread2 = PeopleDetector("rtsp://admin:Poltekpelsorong1@192.168.0.5:554/Streaming/channels/2/")
        self.detector_thread2.start()
        self.isDark = False

    def run(self,*args,**kwargs):
        while True:
            if mqtt.isautomatic:
                if self.detector_thread.setLightOff and self.detector_thread2.setLightOff:
                    if mqtt.get_last_light() > lowest_light_value:
                        mqtt.light = lowest_light_value
                        set_light(lowest_light_value,lowest_light_value)
                        set_temp(0)
                        self.isDark = True
                else:
                    if mqtt.get_last_light() < highest_light_value and self.isDark==True:
                        mqtt.light = highest_light_value 
                        set_light(highest_light_value,highest_light_value)
                        set_temp(20)
                        self.isDark = False