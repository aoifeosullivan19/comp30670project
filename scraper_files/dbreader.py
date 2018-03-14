import mysql
import mysql.connector

db = mysql.connector.connect(host="localhost", user="root", password="", db="test1")
cur = db.cursor()
cur.execute("SELECT * FROM example")
for row in cur.fetchall():
    print (row[0], " ", row[1])
