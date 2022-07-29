from .sql import db_engine
from loguru import logger

class SmokeHandler():
    def __init__(self) -> None:
        self._tab_name = "smoke_log"
    
    def insert_smoke_once(self,value : float):
        try:
            db_engine.insert_one(self._tab_name, value)
        except Exception as e:
            logger.info(f"error when try to insert data with detail {e}")