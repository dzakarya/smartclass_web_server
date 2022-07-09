from fastapi_mqtt.fastmqtt import FastMQTT
from fastapi_mqtt.config import MQTTConfig

mqtt_config = MQTTConfig()
mqtt_client = FastMQTT(config=mqtt_config)