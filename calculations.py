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
    pass

def main():
    cur,conn = set_up_db('FPData.db')
    top5 = get_nba_players(cur,conn)
    nba_comp(top5, cur, conn)
    


if __name__ == "__main__":
    main()