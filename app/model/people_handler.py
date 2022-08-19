from .sql import db_engine
from loguru import logger

class PeopleHandler():
    def __init__(self) -> None:
        self._tab_name = "people_log"
    
    def insert_people_once(self,value : int):
        try:
            db_engine.insert_one(self._tab_name, value)
            logger.info(f"Success insert people data with value : {value}")
        except Exception as e:
            logger.error(f"error when try to insert data with detail {e}")
            
    def get_data(self, date :str, hour:str):
        try:
            db_engine.search_data(self._tab_name,date,hour)
        except Exception as e:
            logger.error(f"error when try to get data with detail {e}")