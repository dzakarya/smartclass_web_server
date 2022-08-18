from .mqtt import mqtt
from config.constant import smoke_topic

def set_smoke(value : int):
    try:
        result = mqtt.publish(f'out_{smoke_topic}', str(value))
    except Exception as e:
        return e
    return result

def get_smoke():
    try:
        result = mqtt.smoke
    except Exception as e:
        return e
    return result