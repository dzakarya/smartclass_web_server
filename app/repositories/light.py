from .mqtt import mqtt
from ..config.constant import light_topic
import RPi.GPIO as GPIO
from loguru import logger

class LightRepository():
    def __init__(self) -> None:
        self._zone1_pin = 12
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._zone1_pin,GPIO.OUT)
        self._pwm_zone1 = GPIO.PWM(self._zone1_pin,1000)
        self._zone1_value = 0
        self._pwm_zone1.start(self._zone1_value)

    def set_light(self,value : int):
        try:
            self._pwm_zone1.ChangeDutyCycle(value)
        except Exception as e:
            logger.error(e)

    def get_light():
        try:
            result = mqtt.light
        except Exception as e:
            return e
        return result