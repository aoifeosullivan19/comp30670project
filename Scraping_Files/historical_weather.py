import requests
import mysql.connector
from mysql.connector import errorcode
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
import csv

Session = sessionmaker()

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


def insert_weather(temp, temp_min, temp_max, description, mainDescription, speed, deg, dt_txt, humidity, rain):
    try:
        connection = engine.connect()
        connection.execute(
            "INSERT INTO weather_info (temp, temp_min, temp_max, description, mainDescription, speed, deg, dt_txt, humidity, rain) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
            (temp, temp_min, temp_max, description, mainDescription, speed, deg, dt_txt, humidity, rain))
    except Exception as e:
        print("An error occurred inserting data into weather_info : ", e)
    return

def get_data():
    with open('dublin_weather.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        #skip over the first row in csv (column header)
        next(csv_reader)
        temperatures = []
        clouds = []
        dt_isos = []
        humidities = []
        min_temps = []
        max_temps = []
        maindescriptions = []
        winds = []
        windspeeds = []
        detdescriptions = []
        rain3hs = []
        for line in csv_reader:
            cloud = line[1]
            dt_iso = line[3]
            humidity = line[4]
            temperature = line[6]
            max_temperature = line[7]
            min_temperature = line[8]
            rain3h = line[11]
            wind = line[12]
            windspeed = line[13]
            detdescription = line[14]
            maindescription = line[17]
            temperatures.append(temperature)
            clouds.append(cloud)
            dt_isos.append(dt_iso)
            humidities.append(humidity)
            min_temps.append(min_temperature)
            max_temps.append(max_temperature)
            maindescriptions.append(maindescription)
            winds.append(wind)
            windspeeds.append(windspeed)
            detdescriptions.append(detdescription)
            rain3hs.append(rain3h)
        length = len(temperatures)
    i = 0
    while i < length:
        var1 = float(temperatures[i])
        truetemp = var1 - 273.15
        var2 = rain3hs[i]
        var3 = dt_isos[i]
        var4 = humidities[i]
        var5 = float(min_temps[i])
        truemin = var5 - 273.15
        var6 = float(max_temps[i])
        truemax = var6 - 273.15
        var7 = maindescriptions[i]
        var8 = winds[i]
        var9 = windspeeds[i]
        var10 = detdescriptions[i]
        insert_weather(truetemp, truemin, truemax, var10, var7, var9, var8, var3, var4, var2)
        i += 1
        # https://www.youtube.com/watch?v=K_oXb04izZM

engine = connect()
get_data()
