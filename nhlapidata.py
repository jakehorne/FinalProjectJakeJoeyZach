import requests
import json
import sqlite3
import os

def player_data():
    '''
    This function has no input or output.
    It references an api and returns a list of tuples. 
    These tuples include a player id, name, team abbreviation, and team.
    '''
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
    '''
    This function takes in a database name and sets up a database under that name. 
    It returns the cur and conn which can be used to access and change the database.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def add_players(data,cur,conn):
    '''
    This function takes in cur, conn and the data returned by player_data. 
    It then adds each tuple to the nhl_ids table.
    '''
    cur.execute("CREATE TABLE IF NOT EXISTS nhl_ids('player_id' INTEGER PRIMARY KEY,'name' TEXT, 'abbreviation' TEXT, 'team' TEXT)") 
    conn.commit()
    for tup in data:
        cur.execute("INSERT OR IGNORE INTO nhl_ids(player_id,name,abbreviation,team) VALUES(?,?,?,?)", (tup[0],tup[1],tup[2],tup[3]))

def main():
    cur,conn = set_up_db('FPData.db')
    players = player_data()
    print(players)
    #list_ids = [tup[0] for tup in players]
    a,b = 0,25
    while b <= 850:
        data = players[a:b]
        add_players(data,cur,conn)

    


if __name__ == "__main__":
    main()


