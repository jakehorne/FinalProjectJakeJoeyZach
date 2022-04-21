import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np

def set_up_db(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def get_nba_players(cur,conn):
    cur.execute('''Select name,team,ppg FROM NBAWebData
                LIMIT 5''')
    return cur.fetchall()

def get_team_avg(team, cur, conn):
    cur.execute('''SELECT NBAData.points, nba_ids.team
                FROM NBAData JOIN nba_ids
                ON nba_ids.player_id = NBAData.player_id''')
    data = cur.fetchall()
    points = 0
    count = 0
    for tup in data:
        if tup[1] == team:
            points += tup[0]
            count += 1
    return round(points/count,2)

def nba_comp(top5, cur, conn):
    list_list = []
    list_pts = []
    for player in top5:
        list_list.append([player[0], player[1]])
        teamppg = get_team_avg(player[1], cur, conn)
        list_pts.append([player[2], teamppg])
    fig, ax = plt.subplots()
    ax.bar(list_list[0],list_pts[0])
    ax.bar(list_list[1],list_pts[1])
    ax.bar(list_list[2],list_pts[2])
    ax.bar(list_list[3],list_pts[3])
    ax.bar(list_list[4],list_pts[4])
    ax.set_xlabel('Player or Team')
    ax.set_ylabel('Points Per Game')
    ax.set_title('5 Leading NBA Scorers Versus Their Team Averages')
    fig.set_figheight(5)
    fig.set_figwidth(10)
    plt.tight_layout()
    fig.savefig("NBAPlayerVteam.png")
    plt.show()
    pass

def nba_graph(cur,conn):
    cur.execute("SELECT team FROM NBAWebData")
    dict_teams = {}
    data = cur.fetchall()
    for tup in data:
        team = tup[0]
        dict_teams[team] = dict_teams.get(team, 0) + 1
    sorted_data = sorted(dict_teams.items(), key  = lambda x: x[1])
    teams = []
    players = []
    for tup in sorted_data:
        teams.append(tup[0])
        players.append(tup[1])
    fig, ax = plt.subplots()
    ax.bar(teams,players)
    ax.set_xlabel('Team')
    ax.set_ylabel('# of Players in Top 100 PPG')
    ax.set_title('Teams With Players in Top 100 PPG')
    fig.set_figheight(5)
    fig.set_figwidth(15)
    plt.tight_layout()
    fig.savefig("NBATeams.png")
    plt.show()
    pass

def nhl_graph(cur,conn):
    cur.execute('''SELECT abbreviation
                FROM nhl_ids JOIN nhl_data
                ON nhl_data.name.split()[1] in nhl_ids''')
    print(cur.fetchall())

def main():
    cur,conn = set_up_db('FPData.db')
    top5 = get_nba_players(cur,conn)
    nba_comp(top5, cur, conn)
    nba_graph(cur,conn)
    nhl_graph(cur,conn)



if __name__ == "__main__":
    main()