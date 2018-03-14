#http://datascience-enthusiast.com/R/AWS_RDS_R_Python.html
import pandas as pd
import mysql.connector
from mysql.connector import errorcode

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
     
databasename=connect()
create_table(databasename)
