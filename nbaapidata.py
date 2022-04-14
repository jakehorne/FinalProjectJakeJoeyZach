import requests
import json
import sqlite3
import os

def player_data(a,b):
    list_data = []
    url = "https://www.balldontlie.io/api/v1/season_averages?player_ids[]={}"
    for i in range(a,b):
        request_url = url.format(i)
        r = requests.get(request_url)
        data = r.text
        try:
            dict = json.loads(data)
            if len(dict["data"]) > 0:
                list_data.append(dict['data'][0])
        except:
            continue
    return list_data

def set_up_db(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def add_to_db(data, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS NBAData ('player_id' INTEGER PRIMARY KEY, 'points' INTEGER, 'rebounds' INTEGER, 'assists' INTEGER)")
    conn.commit()
    for i in data:
        player_id = i['player_id']
        points = i['pts']
        rebounds = i['reb']
        assists = i['ast']
        cur.execute('INSERT OR IGNORE INTO NBAData (player_id,points,rebounds,assists) VALUES(?,?,?,?)', (player_id,points,rebounds,assists))
    conn.commit()

