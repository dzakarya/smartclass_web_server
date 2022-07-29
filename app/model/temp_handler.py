from loguru import logger
from .sql import db_engine

class TempHandler():
    def __init__(self) -> None:
        self._tab_name = "temperature_log"

    def insert_temp_once(self,value : float):
        try:
            db_engine.insert_one(self._tab_name, value)
        except Exception as e:
            logger.info(f"error when try to insert data with detail {e}")
        
     