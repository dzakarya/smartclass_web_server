from loguru import logger
from .sql import db_engine

class TempHandler():
    def __init__(self) -> None:
        self._tab_name = "temperature_log"

    def insert_temp_once(self,value : float):
        try:
            db_engine.insert_one(self._tab_name, value)
            logger.info(f"Success insert temp data with value : {value}")
        except Exception as e:
            logger.error(f"error when try to insert data with detail {e}")
    
    def get_data(self, date :str, hour:str):
        try:
            db_engine.search_data(self._tab_name,date,hour)
        except Exception as e:
            logger.error(f"error when try to get data with detail {e}")
        
     