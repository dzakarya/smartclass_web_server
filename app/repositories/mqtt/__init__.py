from .mqtt import MQTT

mqtt = MQTT()

from ...config.constant import temp_topic, light_topic, smoke_topic
from loguru import logger

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
        elif msg.topic == f'in_{smoke_topic}':
            mqtt.temp = float(msg.payload)
        elif msg.topic == f'in_{light_topic}':
            mqtt.light = float(msg.payload)
    except Exception as e:
        logger.error(e)
    logger.info(f"topic:{msg.topic} payload:{msg.payload}")

mqtt.mqtt_client.username_pw_set(mqtt.mqtt_config["username"],mqtt.mqtt_config["password"])
mqtt.mqtt_client.on_connect = connect
mqtt.mqtt_client.on_message = on_message

mqtt.mqtt_client.connect(mqtt.mqtt_config["host"],mqtt.mqtt_config["port"],60)