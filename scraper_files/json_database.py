import requests
import json
import csv
import time
import schedule
import pandas as pd
import mysql.connector
from mysql.connector import errorcode
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *

#http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
Base = declarative_base()
Session = sessionmaker()
metadata=MetaData()


def data_collector (url):
    """Retrieves information from Dublin Bikes API and stores as JSON"""

    req = requests.get(url)
    req_text= req.text
    json_parsed=json.loads(req_text)
    url="https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=7ad82bb68a98a4a16979023ed867b6501b108e6e"
    return json_parsed

class json_data:
    def data(self):
        for i in json:
            name = i['name']
            number = i['number']
            address=i['address']
            banking=i['banking']
            bike_stands=i['bike_stands']
            
            status=i['status']
            insert_data(name, number, address, banking, bike_stands, status)
    #http://pythondata.com/collecting-storing-tweets-python-mysql/
def connect():
    """Function to connect to database on Amazon Web Services"""

    engine = create_engine('mysql+mysqlconnector://dublinbikesadmin:dublinbikes2018@dublinbikes.cglcinwmtg3w.eu-west-1.rds.amazonaws.com/dublinbikes')    
    port=3306
    connection = engine.connect()
    Session.configure(bind=engine)
    return engine    
    #https://campus.datacamp.com/courses/introduction-to-relational-databases-in-python/advanced-sqlalchemy-queries?ex=2#skiponboarding
    

def create_table(databasename):
    """Function to create new table in given database"""

    metadata=MetaData()

    static_info = Table('static_info', metadata,
        Column ('name', String (60)),
        Column('number', Integer, primary_key=True),
        Column('address', String (60)),
        Column('banking', String (40)),
        Column('bike_stands', Integer),
        Column('status', String (40)))

    metadata.create_all(engine, checkfirst=True)

def insert(databasename, json):
    """Function to insert values into database table"""
    
    connection = engine.connect()     
    connection.execute ("INSERT INTO static_info (name, number, address, banking, bike_stands, status) VALUES (%s, %s, %s, %s, %s, %s);", (name, number, address, banking, bike_stands, status))    
    databasename.commit()
    cursor.close()
    databasename.close()
    return

def insert_data(name, number, address, banking, bike_stands, status):

    connection = engine.connect()
    
    connection.execute ("INSERT INTO static_info (name, number, address, banking, bike_stands, status) VALUES (%s, %s, %s, %s, %s, %s);", (name, number, address, banking, bike_stands, status))
    return



url="https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=7ad82bb68a98a4a16979023ed867b6501b108e6e"
json=data_collector(url)
engine=connect()
create_table(engine)
test=json_data()
test.data()

#https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_sql.html 
