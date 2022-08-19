from .mqtt import mqtt
from config.constant import light_topic,lowest_light_value,highest_light_value

def set_light(zone1 : float, zone2 : float):
    if zone1<=lowest_light_value:
        zone1=lowest_light_value
    if zone1>=highest_light_value:
        zone1=highest_light_value

    if zone2<=lowest_light_value:
        zone2=lowest_light_value
    if zone2>=highest_light_value:
        zone2=highest_light_value

    try:
        result = mqtt.publish(f'out_{light_topic}', f"{zone1}-{zone2}")
    except Exception as e:
        return e
    return result

def get_light():
    try:
        result = mqtt.light
    except Exception as e:
        return e
    return result