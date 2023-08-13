import sqlite3
import pandas as pd

class DB:
    def __init__(self):
        self.dbname = ("HighScore.db")
        con = sqlite3.connect(self.dbname, isolation_level=None)
        cur = con.cursor()
        cur.execute("create table if not exists HighScore(user_name text primary key, high_score integer not null, date text)")
        con.close()
    
    def delete(self):
        con, cur = self.connect()
        con.execute("drop table if exists HighScore")
        con.commit()
        con.close()

    def connect(self):
        con = sqlite3.connect(self.dbname, isolation_level=None)
        return con, con.cursor()
    
    def insert(self, data):
        con, cur = self.connect()
        cur.execute("insert into HighScore values(?, ?, ?)", data)
        con.commit()
        con.close()

    def update(self, data):
        con, cur = self.connect()
        user_name, high_score, date = data
        cur.execute(f"update HighScore set high_score='{high_score}', date='{date}' where user_name='{user_name}'")
        con.close()
    
    def query(self, user_name):
        con, cur = self.connect()
        df = pd.read_sql_query(f"select * from HighScore where user_name in('{user_name}')", con)
        con.close()
        return df
    
    def load(self):
        con, cur = self.connect()
        df = pd.read_sql("select * from HighScore", con)
        con.close()
        return df
    
    def sort_load(self):
        con, cur = self.connect()
        df = pd.read_sql_query("select * from HighScore order by date asc", con)
        con.close()
        df = df.sort_values(by="high_score", ascending=False)
        return df
