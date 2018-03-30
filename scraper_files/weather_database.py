import requests
import json
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
import call_weather_api as ca
import pymysql

# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
Base = declarative_base()
Session = sessionmaker()
metadata = MetaData()


class json_data:
    def data(self):
        for i in json_weather:
            message = i['message']
            list = i['list']
            main = list['main']
            temp = main['temp']
            temp_min = main['temp_min']
            temp_max = main['temp_max']
            weather = list['weather']
            maindescrip = weather['main']
            description = weather['description']
            wind = list['wind']
            speed = wind['speed']
            deg = wind['deg']
            dt_txt = list['dt_txt']

        insert_weather(temp, temp_min, temp_max, speed, maindescrip, description, deg, dt_txt)

    # http://pythondata.com/collecting-storing-tweets-python-mysql/



def connect():
    """Function to connect to database on Amazon Web Services"""
    try:
        engine = create_engine(
            'mysql+mysqlconnector://MuireannMacC:muireannpassword@testdb.cxb1icy6ikcz.us-east-2.rds.amazonaws.com/TestDataBase')
        port = 3306
        connection = engine.connect()
        Session.configure(bind=engine)
        print("Connection successful")
    except Exception as e:
        print("Oops...unable to connect to database at present")
        print(e)
    return engine
    # https://campus.datacamp.com/courses/introduction-to-relational-databases-in-python/advanced-sqlalchemy-queries?ex=2#skiponboarding


def create_table(databasename):
    """Function to create new table in given database"""

    metadata = MetaData()

    weather_info = Table('weather_info', metadata,
                        Column('temp', Float(40)),
                        Column('temp_min', Float(40)),
                        Column('temp_max', Float(40)),
                        Column('maindescrip', String(40)),
                        Column('description', String(40)),
                        Column('speed', Float(40)),
                        Column('deg', Float(40)),
                        Column('dt_txt', String(40)))
    metadata.create_all(engine, checkfirst=True)

    # http://docs.sqlalchemy.org/en/latest/core/metadata.html


def insert_weather(temp, temp_min, temp_max, speed, maindescrip, description, deg, dt_txt):
    connection = engine.connect()
    connection.execute(
        "INSERT INTO weather_info (temp, temp_min, temp_max, speed, maindescrip, description, deg, dt_txt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
        (temp, temp_min, temp_max, speed, maindescrip, description, deg, dt_txt))
    return



url = "http://api.openweathermap.org/data/2.5/forecast?id=5344157&APPID=c8610607135716bfdae60b788f8e0c8d"
engine = connect()
create_table(engine)
weatherData = ca.call_weather_api(url)
json_weather = ca.write_weather(weatherData)
# https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_sql.html

