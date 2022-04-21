import requests
import json
import sqlite3
import os
from bs4 import BeautifulSoup

def set_up_db(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def get_nhl(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "html.parser")
    stats = soup.find_all("tr")
    list_data = []
    for stat in stats:
        list_data.append(stat.text.split())
    return list_data

def clean_data(data):
    new_data = []
    for lst in data[1:]:
        rank = int(lst[0])
        points = int(lst[4])
        name = lst[1] + ' ' + lst[2]
        new_data.append((rank, name, points))
    return new_data

def main():
    cur, conn = set_up_db("FPData.db")
    data1 = get_nhl('http://www.nhl.com/ice/m_statslist.htm?view=points')
    data2 = get_nhl('http://www.nhl.com/ice/m_statslist.htm?season=20212022&view=points&pg=2')
    data3 = get_nhl('http://www.nhl.com/ice/m_statslist.htm?season=20212022&view=points&pg=3')
    data4 = get_nhl('http://www.nhl.com/ice/m_statslist.htm?season=20212022&view=points&pg=4')
    data5 = get_nhl('http://www.nhl.com/ice/m_statslist.htm?season=20212022&view=points&pg=5')
    print(clean_data(data1))

if __name__ == "__main__":
    main()
