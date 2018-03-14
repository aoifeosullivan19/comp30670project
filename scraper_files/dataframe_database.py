#!/home/ubuntu/anaconda3/bin/python

import requests
import json
import time
import csv
import pandas as pd

url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=7ad82bb68a98a4a16979023ed867b6501b108e6e"
req = requests.get(url)
req_text= req.text
json_parsed=json.loads(req_text)
df =pd.read_json(req_text)

#json_parsed/csv_data

for i in json_parsed:
    address=i['address']
    name=i['name']
    position=i['position']
    banking=i['banking']
    status=i['status']
    contract_name=i['contract_name']
    bike_stands=i['bike_stands']
    available_bike_stands=i['available_bike_stands']
    available_bikes=i['available_bikes']
    last_update=i['last_update']
    number=i['number']
    bonus=i['bonus']

import mysql
import csv
from mysql.connector import errorcode
import mysql


db = mysql.connector.connect(host="dublinbikes.cglcinwmtg3w.eu-west-1.rds.amazonaws.com", port=3306, user="dublinbikesadmin", db="dublinbikes", password="dublinbikes2018", database='dublinbikes')
engine = mysql.connector.connect(host="dublinbikes.cglcinwmtg3w.eu-west-1.rds.amazonaws.com", port=3306, user="dublinbikesadmin", db="dublinbikes", password="dublinbikes2018", database='dublinbikes')
connection=engine.connect()
name='realtime_data'
cursor = engine.cursor(dictionary=True)

query="INSERT INTO realtime_data (name, address, position, banking, bonus, status, contract_name, bike_stands, available_bike_stands, available_bikes, last_update) VALUES('1', 'test1', 'test1', 't1', 'test1', 'test1', 'test1', 'test1', 'test1', 'test1', 'test1', 'test1')"

cursor.execute(query, [i['name'], i['address'], i['position'], i['banking'], i['bonus'], i['status'], i['contract_name'], i['bike_stands'], i['available_bike_stands'], i['available_bikes'], i['last_update']])
engine.commit()
cursor.close()
db.close()
