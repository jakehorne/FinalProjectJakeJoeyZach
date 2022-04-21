import requests
import json
import sqlite3
import os

def set_up_db(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def main():
    cur, conn = set_up_db("FPData.db")

if __name__ == "__main__":
    main()
