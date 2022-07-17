from loguru import logger
import paho.mqtt.client as mqtt
class MQTT():
    def __init__(self) -> None:
        self.temp = 0
        self.light = 0
        self.smoke = 0
        self.mqtt_config ={
            "host":"192.168.100.79",
            "port":1883,
            "username":"smartclass",
            "password":"jone"
        }
        self.mqtt_client = mqtt.Client()

    def publish(self, topic:str, msg:str):
        res = self.mqtt_client.publish(topic,msg)
        if res[0] == 0:
            logger.info(f'Succes send {msg} with topic {topic}')
        else:
            logger.error(f'Failed to send {msg} with topic {topic}')
        return res[0]