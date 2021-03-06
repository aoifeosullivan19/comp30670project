import requests
import json
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
import datetime
import call_api as ca 

#http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
Base = declarative_base()
Session = sessionmaker()
metadata=MetaData()

class json_data:
    def data(self):
        for i in json_parsed:
            name = i['name']
            number = i['number']
            address=i['address']
            banking=i['banking']
            position=i['position']
            latitude=position['lat']
            longitude=position['lng']
            bike_stands=i['bike_stands']
            status=i['status']
            insert_data(name, number, address, banking, latitude, longitude, bike_stands, status)
    #http://pythondata.com/collecting-storing-tweets-python-mysql/
    

    def dynamic(self):            
    #https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date-in-python

        for i in json_parsed:
            number = i['number']
            available_bike_stands=i['available_bike_stands']
            last_update=datetime.datetime.fromtimestamp(i['last_update']/1000)
            available_bikes=i['available_bikes']
            insert_dynamic(number, available_bike_stands, last_update, available_bikes)
    #http://pythondata.com/collecting-storing-tweets-python-mysql/


    def latest(self):
        for i in json_parsed:
            number = i['number']
            available_bike_stands=i['available_bike_stands']
            last_update=i['last_update']
            available_bikes=i['available_bikes']
            insert_latest(number, available_bike_stands, last_update, available_bikes)
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
        Column('latitude', Float(40)),
        Column('longitude', Float(40)),
        Column('banking', String (40)),
        Column('bike_stands', Float(40)),
        Column('status', String (40)))
     
    dynamic_info=Table('dynamic_info', metadata,
        Column('number', Integer, ForeignKey("static_info.number")),
        Column('available_bike_stands', Float(40)),
        Column('last_update', String (100)),
        Column('available_bikes', Float(40)))

    latest_info=Table('latest_info', metadata,
        Column('number', Integer, ForeignKey("static_info.number")),
        Column('available_bike_stands', Float(40)),
        Column('last_update', String(100)),
        Column('available_bikes', Float(40)))

    metadata.create_all(engine, checkfirst=True)

    #http://docs.sqlalchemy.org/en/latest/core/metadata.html

def insert_data(name, number, address, banking, latitude, longitude, bike_stands, status):

    connection = engine.connect()    
    connection.execute ("INSERT INTO static_info (name, number, address, banking, latitude, longitude, bike_stands, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", (name, number, address, banking, latitude, longitude, bike_stands, status))
    return


def insert_dynamic(number, available_bike_stands, last_update, available_bikes):

    connection = engine.connect()
    connection.execute ("INSERT INTO dynamic_info (number, available_bike_stands, last_update, available_bikes) VALUES (%s, %s, %s, %s);", (number, available_bike_stands, last_update, available_bikes))    
    return

def insert_latest(number, available_bike_stands, last_update, available_bikes):

    connection = engine.connect()
    connection.execute ("REPLACE INTO latest_info (number, available_bike_stands, last_update, available_bikes) VALUES (%s, %s, %s, %s);", (number, available_bike_stands, last_update, available_bikes))    
    return


def job():
    """Runs the convert to csv function"""
    url="https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=7ad82bb68a98a4a16979023ed867b6501b108e6e"
    ca.call_api(url)
    data=ca.call_api(url)
    ca.write_file (data)
    json_parsed=ca.write_file(data)
    test=json_data()
    test.dynamic()
 

url="https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=7ad82bb68a98a4a16979023ed867b6501b108e6e"
engine=connect()
create_table(engine)
data=ca.call_api(url)
json_parsed=ca.write_file(data)
job()
#https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_sql.html 

