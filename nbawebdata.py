from bs4 import BeautifulSoup
import requests
import sqlite3
import os


def ppg_2021():
    result = requests.get('https://www.cbssports.com/nba/stats/player/scoring/nba/regular/all-pos/qualifiers/?sortdir=descending&sortcol=ppg')
    #print(result.status_code)
    src = result.content
    soup = BeautifulSoup(src,'lxml')
    #links = soup.find_all('td', class_='right')
    #print(links)
    lst = []
    book_title = soup.find_all('tr',class_="TableBase-bodyTr")
   
    x = 0
    for i in book_title:
        a = (i.text.strip().split())
        lst.append(a)
        x += 1
        if x == 50:
            break
    
    name = []
    team = []
    ppg = []
 
   
    result = requests.get('https://www.cbssports.com/nba/stats/player/scoring/nba/regular/all-pos/qualifiers/?sortdir=descending&sortcol=ppg&page=2')
    src = result.content
    soup = BeautifulSoup(src,'lxml')
    book_title = soup.find_all('tr',class_="TableBase-bodyTr")
    for i in book_title:
        a = (i.text.strip().split())
        lst.append(a)
        x += 1
        if x == 50:
            break
    for i in lst:
        name.append(i[1])
        team.append(i[3])
        if "Jr." in i or "IV" in i:
            ppg.append(i[13])
        else:
            ppg.append(i[11])
    rank=[]
    for i in range(1,151):
        rank.append(i)
    stats = zip(rank,name,team,ppg)
    return tuple(stats)

def set_up_db(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def add_to_db(data, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS NBAWebData ('rank' INTEGER PRIMARY KEY, 'name' STRING, 'team' STRING, 'ppg' INTEGER)")
    conn.commit()
    for i in data:
        print(i)
        rank = i[0]
        name = i[1]
        team = i[2]
        ppg = i[3]
        cur.execute('INSERT OR IGNORE INTO NBAWebData (rank,name,team,ppg) VALUES(?,?,?,?)', (rank,name,team,ppg))
    conn.commit()


def main():
    cur, conn = set_up_db("FPData.db")
    data = ppg_2021()
    add_to_db(data[:25],cur,conn)
    add_to_db(data[25:50],cur,conn)
    add_to_db(data[50:75],cur,conn)
    add_to_db(data[75:],cur,conn)
  

if __name__ == "__main__":
    main()


