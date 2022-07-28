from ..config.constant import *
import mysql.connector

class DB():
    def __init__(self) -> None:
        self.conn = mysql.connector.connect(
            database=db_name,
            host=db_host,
            user=db_user,
            password=db_password
        ) 

    
    def insert_one(self, tab_name :str, value :float):
        cur = self.conn.cursor()
        query = """INSERT INTO temperature_log (created_at, value) VALUES(%s,%s)"""
        val = ("jan",16)
        cur.execute(query,val)
        self.conn.commit()
        count = cur.rowcount
        print(count, "Record inserted successfully")