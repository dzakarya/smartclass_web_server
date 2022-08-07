from .mqtt import mqtt
from ..config.constant import light_topic

def set_light(zone1 : float, zone2 : float):
    try:
        result = mqtt.publish(f'out_{light_topic}', f"zone1:{zone1}-zone2:{zone2}")
    except Exception as e:
        return e
    return result

def get_light():
    try:
        result = mqtt.light
    except Exception as e:
        return e
    return result