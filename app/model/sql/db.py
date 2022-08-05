from ...config.constant import *
import mysql.connector
from datetime import datetime
class DB():
    def __init__(self) -> None:
        config = {
            'database' : db_name,
            'host':db_host,
            'user':db_user,
            'password':db_password
        }
        self.conn = mysql.connector.connect(**config
        ) 

    
    def insert_one(self, tab_name :str, value :float):
        cur = self.conn.cursor()
        now = datetime.now(tz)
        date = now.strftime('%d-%m-%Y')
        hour = now.strftime('%H:%M')
        query = f"""INSERT INTO {tab_name} (date, time, value) VALUES(%s,%s,%s)"""
        val = (date,hour,value)
        cur.execute(query,val)
        self.conn.commit()
        count = cur.rowcount

    def search_data(self, tab_name :str,  date :str, hour :str):
        cur = self.conn.cursor()
        query = f"""SELECT * FROM {tab_name} where date = %s and hour = %s"""
        val = (date,hour)
        cur.execute(query,val)
        return cur.fetchall()
