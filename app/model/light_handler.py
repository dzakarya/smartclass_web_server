from .sql import db_engine
from loguru import logger

class LightHandler():
    def __init__(self) -> None:
        self._tab_name = "light_log"
    
    def insert_light_once(self,value : float):
        try:
            db_engine.insert_one(self._tab_name, value)
        except Exception as e:
            logger.info(f"error when try to insert data with detail {e}")