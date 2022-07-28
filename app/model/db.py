from ..config.constant import *
import psycopg2

class DB():
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            database=db_name,
            host=db_host,
            user=db_user,
            password=db_password,
            port=db_port
        ) 

        self.conn.autocommit = True
    
    def insert_one(self, tab_name :str, value :float):
        cur = self.conn.cursor()
        query = """INSERT INTO temperature_log (created_at, value) VALUES(%s,%s)"""
        val = ("jan",16)
        cur.execute(query,val)
        self.conn.commit()
        count = cur.rowcount
        print(count, "Record inserted successfully")