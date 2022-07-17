from .mqtt import mqtt
from ..config.constant import temp_topic

def set_temp(value : int):
    try:
        result = mqtt.publish(f'out_{temp_topic}', str(value))
    except Exception as e:
        return e
    return result

def get_temp():
    try:
        result = mqtt.temp
    except Exception as e:
        return e
    return result