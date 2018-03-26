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
import pytz

#http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
Base = declarative_base()
Session = sessionmaker()
metadata=MetaData()

class json_data:
   
    def latest(self):
        for i in json_parsed:
            number = i['number']
            available_bike_stands=i['available_bike_stands']
            last_update=datetime.datetime.fromtimestamp(i['last_update']/1000, pytz.timezone('Europe/Dublin'))            
            available_bikes=i['available_bikes']
            insert_latest(number, available_bike_stands, last_update, available_bikes)
    #http://pythondata.com/collecting-storing-tweets-python-mysql/

    def delete_latest(self):
        for i in json_parsed:
            number = i['number']
            available_bike_stands=i['available_bike_stands']
            last_update=datetime.datetime.fromtimestamp(i['last_update']/1000, pytz.timezone('Europe/Dublin'))
            available_bikes=i['available_bikes']
            delete_rows(number, available_bike_stands, last_update, available_bikes)
    #http://pythondata.com/collecting-storing-tweets-python-mysql/

def connect():
    """Function to connect to database on Amazon Web Services"""

    engine = create_engine('mysql+mysqlconnector://dublinbikesadmin:dublinbikes2018@dublinbikes.cglcinwmtg3w.eu-west-1.rds.amazonaws.com/dublinbikes')    
    port=3306
    connection = engine.connect()
    Session.configure(bind=engine)
    return engine    
    #https://campus.datacamp.com/courses/introduction-to-relational-databases-in-python/advanced-sqlalchemy-queries?ex=2#skiponboarding

def delete_rows (number, available_bike_stands, last_update, available_bikes):
    
    connection = engine.connect()
    connection.execute("TRUNCATE TABLE latest_info;")
    return

def insert_latest(number, available_bike_stands, last_update, available_bikes):

    connection = engine.connect()
    connection.execute ("INSERT INTO latest_info (number, available_bike_stands, last_update, available_bikes) VALUES (%s, %s, %s, %s);", (number, available_bike_stands, last_update, available_bikes))    
    return
 

url="https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=7ad82bb68a98a4a16979023ed867b6501b108e6e"
engine=connect()
data=ca.call_api(url)
json_parsed=ca.write_file(data)
test=json_data()
test.delete_latest()
test.latest()

#https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_sql.html 
