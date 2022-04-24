import requests
import json
import sqlite3
import os
from bs4 import BeautifulSoup

def set_up_db(db_name):
    '''
    This function takes in a database name and sets up a database under that name. 
    It returns the cur and conn which can be used to access and change the database.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def get_nhl(link):
    '''
    This function takes in a website link.
    It returns a list of values including the rank, player, team, and points.
    '''
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "html.parser")
    stats = soup.find_all("tr")
    list_data = []
    for stat in stats:
        list_data.append(stat.text.split())
    return list_data

def clean_data(data,cur,conn):
    '''
    This function takes in cur, conn, and the data return from get_nhl.
    It then sorts through the data to return of list of tuples.
    Each tuple contains a rank, name, and points.
    Thesetuples are then inserted into the create datab
    '''
    cur.execute("CREATE TABLE IF NOT EXISTS nhl_data('rank' INTEGER PRIMARY KEY, 'name' TEXT, 'points' INTEGER)")
    conn.commit()
    new_data = []
    for lst in data[1:]:
        rank = int(lst[0])
        points = int(lst[4])
        name = lst[2]
        cur.execute("INSERT OR IGNORE INTO nhl_data(rank,name,points) VALUES(?,?,?)", (rank, name, points))
        conn.commit()
        new_data.append((rank, name, points))
    return new_data


def main():
    cur, conn = set_up_db("FPData.db")
    data1 = get_nhl('http://www.nhl.com/ice/m_statslist.htm?view=points')
    print(data1)
    data2 = get_nhl('http://www.nhl.com/ice/m_statslist.htm?season=20212022&view=points&pg=2')
    data3 = get_nhl('http://www.nhl.com/ice/m_statslist.htm?season=20212022&view=points&pg=3')
    data4 = get_nhl('http://www.nhl.com/ice/m_statslist.htm?season=20212022&view=points&pg=4')
    data5 = get_nhl('http://www.nhl.com/ice/m_statslist.htm?season=20212022&view=points&pg=5')
    clean_data(data1,cur,conn)
    clean_data(data2,cur,conn)
    clean_data(data3,cur,conn)
    clean_data(data4,cur,conn)
    clean_data(data5,cur,conn)

    

if __name__ == "__main__":
    main()
