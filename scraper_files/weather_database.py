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
import call_weather_api as ca

# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
Base = declarative_base()
Session = sessionmaker()
metadata = MetaData()


class json_data:
    def data(self):
        list = json_weather['list']
        #i = 0
        length = len(list)
        #while i < length:
        access = list[0]
        main = access['main']
        temp = main['temp']
        temp_min = main['temp_min']
        temp_max = main['temp_max']
        humidity = main['humidity']
        weather = access['weather']
        weathered = weather[0]
        description = weathered['description']
        wind = access['wind']
        speed = wind['speed']
        deg = wind['deg']
        dt_txt = access['dt_txt']
            #print(temp)
            #i += 1
        insert_weather(temp, temp_min, temp_max, description, speed, deg, dt_txt, humidity)
        delete_rows(temp, temp_min, temp_max, description, speed, deg, dt_txt, humidity)
        insert_dynamic_weather(temp, temp_min, temp_max, description, speed, deg, dt_txt, humidity)

    # http://pythondata.com/collecting-storing-tweets-python-mysql/


def connect():
    """Function to connect to database on Amazon Web Services"""
    try:

        engine = create_engine(
            'mysql+mysqlconnector://dublinbikesadmin:dublinbikes2018@dublinbikes.cglcinwmtg3w.eu-west-1.rds.amazonaws.com/dublinbikes')
        port = 3306
        connection = engine.connect()
        Session.configure(bind=engine)
        return engine
        # https://campus.datacamp.com/courses/introduction-to-relational-databases-in-python/advanced-sqlalchemy-queries?ex=2#skiponboarding

    except Exception as err:
        print("An error occurred when connecting to the database: ", err)
        # https://dev.mysql.com/doc/connector-python/en/connector-python-api-errors-error.html
    # https://campus.datacamp.com/courses/introduction-to-relational-databases-in-python/advanced-sqlalchemy-queries?ex=2#skiponboarding


def create_static_table(databasename):
    """Function to create new table in given database"""

    metadata = MetaData()

    weather_info = Table('weather_info', metadata,
                        Column('temp', Float(40)),
                        Column('temp_min', Float(40)),
                        Column('temp_max', Float(40)),
                        Column('description', String(40)),
                        Column('speed', Float(40)),
                        Column('deg', Float(40)),
                        Column('dt_txt', String(60)),
                        Column('humidity', Float(40)))

    metadata.create_all(engine, checkfirst=True)

def create_dynamic_table(databasename):
    """Function to create new table in given database"""

    metadata = MetaData()

    dynamic_weather = Table('dynamic_weather', metadata,
                        Column('temp', Float(40)),
                        Column('temp_min', Float(40)),
                        Column('temp_max', Float(40)),
                        Column('description', String(40)),
                        Column('speed', Float(40)),
                        Column('deg', Float(40)),
                        Column('dt_txt', String(60)),
                        Column('humidity', Float(40)))

    metadata.create_all(engine, checkfirst=True)

    # http://docs.sqlalchemy.org/en/latest/core/metadata.html


def insert_weather(temp, temp_min, temp_max, description, speed, deg, dt_txt, humidity):
    connection = engine.connect()
    connection.execute(
        "INSERT INTO weather_info (temp, temp_min, temp_max, description, speed, deg, dt_txt, humidity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
        (temp, temp_min, temp_max, description, speed, deg, dt_txt, humidity))
    return

def delete_rows(temp, temp_min, temp_max, description, speed, deg, dt_txt, humidity):
        connection = engine.connect()
        connection.execute("TRUNCATE TABLE dynamic_weather;")
        return

def insert_dynamic_weather(temp, temp_min, temp_max, description, speed, deg, dt_txt, humidity):
    connection = engine.connect()
    connection.execute ("INSERT INTO dynamic_weather (temp, temp_min, temp_max, description, speed, deg, dt_txt, humidity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                        (temp, temp_min, temp_max, description, speed, deg, dt_txt, humidity))
    return



url = "http://api.openweathermap.org/data/2.5/forecast?id=2964574&units=metric&APPID=c8610607135716bfdae60b788f8e0c8d"
engine = connect()
create_dynamic_table(engine)
create_static_table(engine)
weatherData = ca.call_weather_api(url)
json_weather = ca.write_weather(weatherData)
run=json_data()
run.data()
# https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_sql.html

