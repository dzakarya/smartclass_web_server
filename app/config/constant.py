import pytz
import os

ROOT_PATH = os.path.join(os.getcwd(), 'app')
DATA_PATH = os.path.join(ROOT_PATH, 'data')

model_path = "/home/smartclass/Desktop/smartclassv2/app/data/detect.tflite"
label_path = "/home/smartclass/Desktop/smartclassv2/app/data/labelmap.txt"
temp_topic = os.getenv("SC_MQTT_TEMP_TOPIC")
light_topic = os.getenv("SC_MQTT_LIGHT_TOPIC")
smoke_topic = os.getenv("SC_MQTT_SMOKE_TOPIC")
mqtt_host = os.getenv("SC_MQTT_HOST")
mqtt_port = int(os.getenv("SC_MQTT_PORT"))
mqtt_username = os.getenv("SC_MQTT_USERNAME")
mqtt_password = os.getenv("SC_MQTT_PASSWORD")
db_name = os.getenv("SC_DB_NAME")
db_user = os.getenv("SC_DB_USER")
db_host = os.getenv("SC_DB_HOST")
db_password = os.getenv("SC_DB_PASSWORD")
tz = pytz.timezone(os.getenv("SC_TIMEZONE"))
lowest_light_value = int(os.getenv("SC_LOWEST_LIGHT_VALUE"))
highest_light_value = int(os.getenv("SC_HIGHEST_LIGHT_VALUE"))