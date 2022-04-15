import requests
import json
import sqlite3
import os
def set_up_db(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def get_team_avg(team, cur, conn):
    cur.execute('''SELECT NBAData.points, nba_ids.team
                FROM NBAData JOIN nba_ids
                ON nba_ids.player_id = NBAData.player_id''')
    data = cur.fetchall()
    points = 0
    count = 0
    for tup in data:
        if tup[1] == team:
            print(tup)
            points += tup[0]
            count += 1
    return round(points/count,2)

def main():
    cur,conn = set_up_db('FPData.db')
    print(get_team_avg("LAL", cur, conn))


if __name__ == "__main__":
    main()