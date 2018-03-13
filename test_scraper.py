#!/home/ubuntu/anaconda3/bin/python

import requests
import json
import time
import csv

url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=7ad82bb68a98a4a16979023ed867b6501b108e6e"
req = requests.get(url)
req_text= req.text
json_parsed=json.loads(req_text)
csv_data=json_parsed[0:]
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

#json_parsed/csv_data

import mysql
import csv
from mysql.connector import errorcode
import mysql

db = mysql.connector.connect(host="dublinbikes.cglcinwmtg3w.eu-west-1.rds.amazonaws.com", port=3306, user="dublinbikesadmin", db="dublinbikes", password="dublinbikes2018", database='dublinbikes')
cursor = db.cursor()

insert_query="""INSERT INTO realtime_data (number, name, address, position, banking, bonus, status, contract_name, bike_stands, available_bike_stands, available_bikes, last_update) VALUES('1', 'test1', 'test1', 't1', 'test1', 'test1', 'test1', 'test1', 'test1', 'test1', 'test1', 'test1')"""
cursor.execute(insert_query)

db.commit()

cursor.close()

