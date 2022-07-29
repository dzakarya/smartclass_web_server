from .mqtt import MQTT

mqtt = MQTT()

from ...config.constant import temp_topic, light_topic, smoke_topic
from loguru import logger
from ...model.light_handler import LightHandler
from ...model.smoke_handler import SmokeHandler
from ...model.temp_handler import TempHandler

def connect(client, userdata, flags, rc):
    mqtt.mqtt_client.subscribe(f'in_{temp_topic}')
    mqtt.mqtt_client.subscribe(f'in_{smoke_topic}')
    mqtt.mqtt_client.subscribe(f'in_{light_topic}')
    logger.info(f"Subscribed to topic in_{temp_topic}")
    logger.info(f"Subscribed to topic in_{smoke_topic}")
    logger.info(f"Subscribed to topic in_{light_topic}")
    logger.info("Connected with result code "+str(rc))

def on_message(client, userdata, msg):
    try:
        if msg.topic == f'in_{temp_topic}':
            mqtt.temp = float(msg.payload)
            THandler = TempHandler()
            THandler.insert_temp_once(mqtt.temp) 
        elif msg.topic == f'in_{smoke_topic}':
            mqtt.smoke = float(msg.payload)
            SHandler = SmokeHandler()
            SHandler.insert_smoke_once(mqtt.smoke)
        elif msg.topic == f'in_{light_topic}':
            mqtt.light = float(msg.payload)
            LHandler = LightHandler()
            LHandler.insert_light_once(mqtt.light)
    except Exception as e:
        logger.error(e)
    logger.info(f"topic:{msg.topic} payload:{msg.payload}")

mqtt.mqtt_client.username_pw_set(mqtt.mqtt_config["username"],mqtt.mqtt_config["password"])
mqtt.mqtt_client.on_connect = connect
mqtt.mqtt_client.on_message = on_message

mqtt.mqtt_client.connect(mqtt.mqtt_config["host"],mqtt.mqtt_config["port"],60)