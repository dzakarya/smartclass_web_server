from .db import DB

db_engine = DB()
db_engine.insert_one("temperature_log",0.13)