import requests
import json
import mysql.connector
from mysql.connector import errorcode
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *

def call_weather_api(url):
    """Calls weather API and returns info"""

    req = requests.get(url)
    return req

def write_weather (weatherData):
    """Retrieves weather information from openweathermap and stores as JSON"""

    req_weather = weatherData.text
    json_weather = json.loads(req_weather)
    print(json_weather)
    return json_weather

# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
Base = declarative_base()
Session = sessionmaker()
metadata = MetaData()


class json_weather_data:
    def weather_data(self):
        list = json_weather['list']
        access = list[0]
        main = access['main']
        temp = main['temp']
        temp_min = main['temp_min']
        temp_max = main['temp_max']
        humidity = main['humidity']
        weather = access['weather']
        weathered = weather[0]
        description = weathered['description']
        mainDescription = weathered['main']
        wind = access['wind']
        speed = wind['speed']
        deg = wind['deg']
        dt_txt = access['dt_txt']
        if 'rain' in access:
            rained = access['rain']
            if '3h' in rained:
                rain = rained['3h']
            else:
                rain = 0.0
        else:
            rain = 0.0
        insert_weather(temp, temp_min, temp_max, description, mainDescription, speed, deg, dt_txt, humidity, rain)
        delete_rows(temp, temp_min, temp_max, description, mainDescription, speed, deg, dt_txt, humidity, rain)
        insert_dynamic_weather(temp, temp_min, temp_max, description, mainDescription, speed, deg, dt_txt, humidity,
                               rain)

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

    except Exception as e:
        print("An error occurred when connecting to the database: ", e)
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
                        Column('mainDescription', String(40)),
                        Column('speed', Float(40)),
                        Column('deg', Float(40)),
                        Column('dt_txt', String(60)),
                        Column('humidity', Float(40)),
                        Column('rain', Float(40)))

    metadata.create_all(engine, checkfirst=True)

def create_dynamic_table(databasename):
    """Function to create new table in given database"""

    metadata = MetaData()

    dynamic_weather = Table('dynamic_weather', metadata,
                        Column('temp', Float(40)),
                        Column('temp_min', Float(40)),
                        Column('temp_max', Float(40)),
                        Column('description', String(40)),
                        Column('mainDescription', String(40)),
                        Column('speed', Float(40)),
                        Column('deg', Float(40)),
                        Column('dt_txt', String(60)),
                        Column('humidity', Float(40)),
                        Column('rain', Float(40)))

    metadata.create_all(engine, checkfirst=True)

    # http://docs.sqlalchemy.org/en/latest/core/metadata.html


def insert_weather(temp, temp_min, temp_max, description, mainDescription, speed, deg, dt_txt, humidity, rain):
    try:
        connection = engine.connect()
        connection.execute(
            "INSERT INTO weather_info (temp, temp_min, temp_max, description, mainDescription, speed, deg, dt_txt, humidity, rain) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
            (temp, temp_min, temp_max, description, mainDescription, speed, deg, dt_txt, humidity, rain))
    except Exception as e:
        print("An error occurred inserting data into weather_info : ", e)
    return


def delete_rows(temp, temp_min, temp_max, description, mainDescription, speed, deg, dt_txt, humidity, rain):
    try:
        connection = engine.connect()
        connection.execute("TRUNCATE TABLE dynamic_weather;")
        return

    except Exception as e:
        print("An error occurred when deleting rows: ", e)

def insert_dynamic_weather(temp, temp_min, temp_max, description, mainDescription, speed, deg, dt_txt, humidity, rain):
    try:
        connection = engine.connect()
        connection.execute(
            "INSERT INTO dynamic_weather (temp, temp_min, temp_max, description, mainDescription, speed, deg, dt_txt, humidity, rain) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
            (temp, temp_min, temp_max, description, mainDescription, speed, deg, dt_txt, humidity, rain))
    except Exception as e:
        print("An error occurred inserting data into dynamic_weather: ", e)
    return

url = "http://api.openweathermap.org/data/2.5/forecast?id=2964574&units=metric&APPID=c8610607135716bfdae60b788f8e0c8d"
engine = connect()
create_dynamic_table(engine)
create_static_table(engine)
weatherData = call_weather_api(url)
json_weather = write_weather(weatherData)
run = json_weather_data()
run.weather_data()
# https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_sql.html
