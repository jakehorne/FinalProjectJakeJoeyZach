import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np
import csv

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
    return list(zip(list_list,list_pts))

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
    ax.set_title('Teams With Players in Top 100 PPG in the NBA')
    fig.set_figheight(5)
    fig.set_figwidth(15)
    plt.tight_layout()
    fig.savefig("NBATeams.png")
    plt.show()
    return list(zip(teams,players))

def nhl_graph(cur,conn):
    cur.execute("SELECT name from nhl_data")
    players = cur.fetchall()
    players_list = []
    for tup in players:
        players_list.append(tup[0])
    cur.execute("SELECT name, abbreviation from nhl_ids")
    data = cur.fetchall()
    team_dict = {}
    for player in players_list:
        for tup in data:
            team = tup[1]
            if player in tup[0]:
                team_dict[team] = team_dict.get(team, 0) + 1
    sorted_data = sorted(team_dict.items(), key  = lambda x: x[1])
    teams = []
    players = []
    for tup in sorted_data:
        teams.append(tup[0])
        players.append(tup[1])
    fig, ax = plt.subplots()
    ax.bar(teams,players)
    ax.set_xlabel('Team')
    ax.set_ylabel('# of Players in Top 100 Points')
    ax.set_title('Teams With Players in Top 100 Points for NHL')
    fig.set_figheight(5)
    fig.set_figwidth(15)
    plt.tight_layout()
    fig.savefig("NHLTeams.png")
    plt.show()
    return sorted_data

def write_data(data):
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, "final_project_data.csv")
    with open(full_path, "w", newline='') as f:
        writer = csv.writer(f, delimiter = ',')
        for tup in data:
            writer.writerow(tup)

def main():
    cur,conn = set_up_db('FPData.db')
    top5 = get_nba_players(cur,conn)
    nba_data = nba_comp(top5, cur, conn)
    nba_data2 = nba_graph(cur,conn)
    nhl_data = nhl_graph(cur,conn)
    write_data(nba_data)
    #write_data(nba_data2)



if __name__ == "__main__":
    main()