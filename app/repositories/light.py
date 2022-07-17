from .mqtt import mqtt
from ..config.constant import light_topic

def set_light(value : int):
    try:
        result = mqtt.publish(f'out_{light_topic}', str(value))
    except Exception as e:
        return e
    return result

def get_light():
    try:
        result = mqtt.light
    except Exception as e:
        return e
    return result