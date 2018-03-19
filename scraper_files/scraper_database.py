import requests
import json
import csv
import time
import schedule
import pandas as pd
import mysql.connector
from mysql.connector import errorcode



def data_collector (url):
    """Retrieves information from Dublin Bikes API and stores as JSON"""

    req = requests.get(url)
    req_text= req.text
    json_parsed=json.loads(req_text)
    return json_parsed

def write_to_csv(filename):
    """Converts parsed json to csv and stores in csv file"""

    csv_data=filename[0:]
    csv1_data = open('test.csv', 'a')
    csvwriter = csv.writer(csv1_data)
    count = 0

    for i in csv_data:
        if count == 0:
            header = i.keys()
            csvwriter.writerow(header)
            count += 1
        csvwriter.writerow(i.values())
    csv1_data.close()

def job():
    """Runs the convert to csv function"""

    write_to_csv(filename)


url="https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=7ad82bb68a98a4a16979023ed867b6501b108e6e"
filename=data_collector(url)

for x in filename:
    number=x['number']
    name=x['name']
    address=x['address']
    position=x['position']
    banking=x['banking']
    bonus=x['bonus']
    status=x['status']
    contract=x['contract_name']
    bikestands=x['bike_stands']
    available_stands=x['available_bike_stands']
    available_bikes=x['available_bikes']
    last_update=x['last_update']
    print (number, name, last_update)
                   
def connect():
    """Function to connect to database on Amazon Web Services"""

    try:

        host="dublinbikes.cglcinwmtg3w.eu-west-1.rds.amazonaws.com"
        port=3306
        conn=mysql.connector.connect(user="dublinbikesadmin", password="dublinbikes2018", host=host, port=port, database="dublinbikes")
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print ("Error: incorrect username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print ("Database does not exist")
        else:
            print (err)

    conn.close()

def read_db(databasename):
    """Function to read from database on AWS"""

    cursor = databasename.cursor()
    cursor.execute("SELECT * FROM realtime_data")
    for row in cursor.fetchall():
        print (row[0])

def create_table(databasename):
    """Function to create new table in given database"""

    cursor = databasename.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS bikesdata (number int(11) NOT NULL PRIMARY KEY, name varchar(125),
        address varchar(135), position varchar(135), banking varchar(135), bonus varchar(135), status varchar(135), contract_name varchar(135), bike_stands int(11), available_bikes_stands int(11), available_bikes int(11), last_update varchar(135))""")
    databasename.commit()

def insert(databasename):
    """Function to insert values into database table"""
    n=10
    nme='test'
    address='test3'
    pos='test4'
    bank='test5'
    bon='test6' 
    stat='test7'
    contract='test8'
    bikess=9
    availst=10
    avail=11
    last=12
    t=(n, nme, address, pos, bank, bon, stat, contract, bikess, availst, avail, last)


    cursor=databasename.cursor()
    query="INSERT INTO bikesdata (number, name, address, position, banking, bonus, status, contract, bikestands, available_stands, available_bikes, last_update) VALUES (%d, %s, %s, %s, %s, %s, %s, %s, %d, %d, %d, %d, %d), t"     
    cursor.execute(query %(number,name, address, position, banking, bonus, status, contract, bikestands, available_stands, available_bikes, last_update))
    databasename.commit()
    cursor.close()
    databasename.close()
    return

databasename=connect()
insert(databasename)
