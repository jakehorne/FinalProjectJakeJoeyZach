import requests
import json
import sqlite3
import os

def player_data():
    url = "https://statsapi.web.nhl.com/api/v1/teams?expand=team.roster"
    r = requests.get(url)
    data = r.text
    dict = json.loads(data)
    list_players = []
    for dic in dict['teams']:
        team = dic['name']
        abv = dic['abbreviation']
        roster = dic['roster']['roster']
        for dictionary in roster:
            player = dictionary['person']['fullName']
            id = dictionary['person']['id']
            list_players.append((id,player,abv,team))
    return list_players

def set_up_db(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def add_players(data,cur,conn):
    cur.execute("CREATE TABLE IF NOT EXISTS nhl_ids('player_id' INTEGER PRIMARY KEY,'name' TEXT, 'abbreviation' TEXT, 'team' TEXT)") 
    conn.commit()
    for tup in data:
        cur.execute("INSERT OR IGNORE INTO nhl_ids(player_id,name,abbreviation,team) VALUES(?,?,?,?)", (tup[0],tup[1],tup[2],tup[3]))

# def get_stats(ids, cur, conn):
#     for id in ids:
#         print(id)
#         url = "https://statsapi.web.nhl.com/api/v1/people/ID/stats"
#         r_url = url.format(id)
#         r = requests.get(url)
#         data = r.text
#         #print(data)
#         dict = json.loads(data)
#         print(dict)
#     return

def main():
    cur,conn = set_up_db('FPData.db')
    players = player_data()
    list_ids = [tup[0] for tup in players]
    # a,b = 0,25
    # while b <= 850:
    #     data = players[a:b]
    #     add_players(data,cur,conn)
    # c,d = 0,25
    # while d <= 850:
    #     ids = list_ids[c:d]
    #     print(get_stats(ids,cur,conn))
    


if __name__ == "__main__":
    main()


