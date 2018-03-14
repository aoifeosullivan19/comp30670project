import requests
import json
import time
import csv
import pandas as pd
from sqlalchemy import create_engine

url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=7ad82bb68a98a4a16979023ed867b6501b108e6e"
req = requests.get(url)
req_text= req.text
json_parsed=json.loads(req_text)
csv_data=json_parsed[0:]
csv1_data = open('test.csv', 'a')
df = pd.read_json(req_text)

csvwriter = csv.writer(csv1_data)


count = 0

for i in csv_data:
    if count == 0:
        header = i.keys()
        csvwriter.writerow(header)
        count += 1
    csvwriter.writerow(i.values())

csv1_data.close()

#json_parsed/csv_data

import mysql
import csv
from mysql.connector import errorcode
import mysql
import mysql.connector

engine = mysql.connector.connect(host="dublinbikes.cglcinwmtg3w.eu-west-1.rds.amazonaws.com", port=3306, user="dublinbikesadmin", db="dublinbikes", password="dublinbikes2018", database='dublinbikes')
cursor = engine.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS realtime_data1 (number INT,
name VARCHAR (60),
address VARCHAR(60),
position VARCHAR (80),
banking VARCHAR (80),
bonus VARCHAR (80),
status VARCHAR (80),
contract_name VARCHAR (80),
bike_stands INT,
available_bike_stands INT,
available_bikes INT,
last_update INT)""")
cursor.close()

df.to_sql('realtime_data1', engine)

cursor.close()
