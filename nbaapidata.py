import requests
import json
import sqlite3
import os

def player_data(a,b):
    '''
    This function takes in two variables representing integers: a and b. 
    The balldontlie api is then referenced and returns a list of tuples. 
    These tuples include a player id along with average points, rebounds, and assists.
    '''
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
    '''
    This function takes in a database name and sets up a database under that name. 
    It returns the cur and conn which can be used to access and change the database.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def add_to_db(data, cur, conn):
    '''
    This function takes in the data returned by player_data. 
    It then adds this data to the database under the NBAData table.
    '''
    cur.execute("CREATE TABLE IF NOT EXISTS NBAData ('player_id' INTEGER PRIMARY KEY, 'points' INTEGER, 'rebounds' INTEGER, 'assists' INTEGER)")
    conn.commit()
    for i in data:
        player_id = i['player_id']
        points = i['pts']
        rebounds = i['reb']
        assists = i['ast']
        cur.execute('INSERT OR IGNORE INTO NBAData (player_id,points,rebounds,assists) VALUES(?,?,?,?)', (player_id,points,rebounds,assists))
    conn.commit()

def get_nba_team(a, b, cur, conn):
    '''
    This function takes in two numbers, a and b, along with cur and conn. 
    The function then takes each player_id from the NBAData table. 
    Using the player_id and the balldontlie api, the function returns 
    a list of tuples containing the player_id and their team's three letter abbreviation.
    '''
    cur.execute("SELECT player_id FROM NBAData")
    list_id = []
    for item in cur.fetchall():
        list_id.append(item[0])
    list_tup = []
    for id in list_id:
        if id > a and id < b:
            try:
                url = 'https://www.balldontlie.io/api/v1/players/{}'
                request_url = url.format(id)
                r = requests.get(request_url)
                dict_data = json.loads(r.text)
                team = dict_data['team']['abbreviation']
                list_tup.append((id,team))
            except:
                continue
    return list_tup

def add_team(tups, cur, conn):
    '''
    This function takes in cur, conn, and the data returned by get_nba_team. 
    The data is then inserted into the nba_ids table and nothing is return.
    '''
    cur.execute("CREATE TABLE IF NOT EXISTS nba_ids('player_id' INTEGER PRIMARY KEY, 'team' TEXT)") 
    conn.commit()
    for tup in tups:
        id = tup[0]
        team = tup[1]
        cur.execute("INSERT OR IGNORE INTO nba_ids(player_id,team) VALUES(?,?)", (id,team))
    conn.commit()

def main():
    cur, conn = set_up_db('FPData.db')
    while a<=350:
        data = player_data(a,b)
        add_to_db(data, cur, conn)
        a += 25
        b += 25
    y,z = 0,25
    while y<=350:
        tups = get_nba_team(y,z,cur,conn)
        add_team(tups, cur, conn)
        y += 25
        z += 25

if __name__ == "__main__":
    main()