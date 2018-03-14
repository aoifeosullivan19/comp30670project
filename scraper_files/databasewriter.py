#https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
import mysql.connector
import csv
from mysql.connector import errorcode
import mysql

db = mysql.connector.connect(host="localhost", user="root", password="", database='dublin_bikes')
cursor = db.cursor()
f=open('test.csv', 'r')
next(f, None)
reader=csv.reader(f)
for row in reader:
    query="INSERT INTO test(number, name, address, position, banking, bonus, status, contract_name, bike_stands, available_bike_stands, available_bikes, last_update) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (nnumber, nname, naddress, nposition, nbanking, nbonus, nstatus, ncontract_name, nbike_stands, navailable_bike_stands, navailable_bikes, nlast_update))
f.close()
db.commit()
cursor.close()
connect.close()
