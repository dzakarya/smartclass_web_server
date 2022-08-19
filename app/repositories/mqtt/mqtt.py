from statistics import mean
from loguru import logger
import paho.mqtt.client as mqtt
from config.constant import *
class MQTT():
    def __init__(self) -> None:
        self._temp = []
        self._light = []
        self._smoke = []
        self.mqtt_config ={
            "host":mqtt_host,
            "port":mqtt_port,
            "username":mqtt_username,
            "password":mqtt_password
        }
        self.mqtt_client = mqtt.Client()

    @property
    def temp(self)->float:
        return mean(self._temp)

    @temp.setter
    def temp(self, value:float):
        self._temp.append(value)

    def clean_temp(self):
        self._temp = []

    @property
    def smoke(self)->float:
        return max(self._smoke)

    @smoke.setter
    def smoke(self, value:float):
        self._smoke.append(value)

    @property
    def light(self)->float:
        return mean(self._light)

    @light.setter
    def light(self, value:float):
        self.light.append(value)

    def light(self):
        self._light = []

    def clean_temp(self):
        self._temp = []

    def clean_smoke(self):
        self._smoke = []

    def publish(self, topic:str, msg:str):
        res = self.mqtt_client.publish(topic,msg)
        if res[0] == 0:
            logger.info(f'Succes send {msg} with topic {topic}')
        else:
            logger.error(f'Failed to send {msg} with topic {topic}')
        return res[0]