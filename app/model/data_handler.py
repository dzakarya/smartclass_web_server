from .sql import db_engine
from loguru import logger

class DataHandler():
    def __init__(self) -> None:
        self._tab_light_name = "light_log"
        self._tab_smoke_name = "smoke_log"
        self._tab_temp_name = "temperature_log"
    
    def get_temp_value(self, date: str, time: str):
        val = db_engine.search_data(self._tab_temp_name, date, time)
        return val
            
    def get_smoke_value(self, date: str, time: str):
        val = db_engine.search_data(self._tab_smoke_name, date, time)
        return val
    
    def get_light_value(self, date: str, time: str):
        val = db_engine.search_data(self._tab_light_name, date, time)
        return val