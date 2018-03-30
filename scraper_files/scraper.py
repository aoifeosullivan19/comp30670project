import requests
import json
import csv
import mysql.connector
from mysql.connector import errorcode
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
import datetime
import pytz

#http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
Base = declarative_base()
Session = sessionmaker()
metadata=MetaData()

def call_api(url):
    """Calls API and returns info from that"""

    req = requests.get(url)
    return req

def write_file (data):
    """Retrieves information from Dublin Bikes API and stores as JSON"""

    req_text= data.text
    json_parsed=json.loads(req_text)
    return json_parsed

def csv_write (data):
    """Writes to CSV file as a backup"""
    
    csv_data=data[0:]
    csv1_data = open('backup.csv', 'a')
    csvwriter = csv.writer(csv1_data)

    count = 0

    for i in csv_data:
        if count == 0:
            header = i.keys()
            csvwriter.writerow(header)
            count += 1
        csvwriter.writerow(i.values())

    csv1_data.close()

    #http://blog.appliedinformaticsinc.com/how-to-parse-and-convert-json-to-csv-using-python/


class json_data:
    def data(self):
        """Selects and creates variables that will be stored in static station info table"""

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
        """Selects and creates variables that will be stored in dynamic station info table"""

        for i in json_parsed:
            number = i['number']
            available_bike_stands=i['available_bike_stands']
            last_update=datetime.datetime.fromtimestamp(i['last_update']/1000, pytz.timezone('Europe/Dublin'))
            available_bikes=i['available_bikes']
            insert_dynamic(number, available_bike_stands, last_update, available_bikes)
    #http://pythondata.com/collecting-storing-tweets-python-mysql/
    #https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date-in-python
    #https://stackoverflow.com/questions/7328630/python-pytz-converting-a-timestamp-string-format-from-one-timezone-to-another

    def latest(self):
        """Selects and creates variables that will be stored in latest station info table"""

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
    
    try:

        engine = create_engine('mysql+mysqlconnector://dublinbikesadmin:dublinbikes2018@dublinbikes.cglcinwmtg3w.eu-west-1.rds.amazonaws.com/dublinbikes')
        port=3306
        connection = engine.connect()
        Session.configure(bind=engine)
        return engine
        #https://campus.datacamp.com/courses/introduction-to-relational-databases-in-python/advanced-sqlalchemy-queries?ex=2#skiponboarding

    except Exception as err:
        print ("An error occurred when connecting to the database: ", err)
        #https://dev.mysql.com/doc/connector-python/en/connector-python-api-errors-error.html


def create_table(databasename):
    """Function to create new tables for static, dynamic and latest station info in database"""

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

    dynamic_info=Table('bike_dynamic', metadata,
        Column('number', Integer, ForeignKey("static_info.number")),
        Column('available_bike_stands', Float(40)),
        Column('last_update', String (100)),
        Column('available_bikes', Float(40)))

    latest_info=Table('latest_info', metadata,
        Column('number', Integer, ForeignKey("static_info.number"), primary_key=True),
        Column('available_bike_stands', Float(40)),
        Column('last_update', String(100), primary_key=True),
        Column('available_bikes', Float(40)))

    metadata.create_all(engine, checkfirst=True)

    #http://docs.sqlalchemy.org/en/latest/core/metadata.html

def insert_data(name, number, address, banking, latitude, longitude, bike_stands, status):

    try:
        connection = engine.connect()
        connection.execute ("INSERT IGNORE static_info (name, number, address, banking, latitude, longitude, bike_stands, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", (name, number, address, banking, latitude, longitude, bike_stands, status))            
        return

    except Exception as err:
        print ("An error occurred when inserting static data: ", err)

def insert_dynamic(number, available_bike_stands, last_update, available_bikes):

    try:
        connection = engine.connect()
        connection.execute ("INSERT INTO bike_dynamic (number, available_bike_stands, last_update, available_bikes) VALUES (%s, %s, %s, %s);", (number, available_bike_stands, last_update, available_bikes))
        return
    
    except Exception as err:
        print ("An error occurred when inserting dynamic info: ", err)
        test.data() #if an error occurs call function that creates static info table as more stations may have been added

def delete_rows (number, available_bike_stands, last_update, available_bikes):
    
    try:
        connection = engine.connect()
        connection.execute("TRUNCATE TABLE latest_info;")
        return

    except Exception as err:
        print ("An error occurred when deleting latest table: ", err)
        test.data()

def insert_latest(number, available_bike_stands, last_update, available_bikes):

    try:
        connection = engine.connect()
        connection.execute ("INSERT INTO latest_info (number, available_bike_stands, last_update, available_bikes) VALUES (%s, %s, %s, %s);", (number, available_bike_stands, last_update, available_bikes))
        return

    except Exception as err:
        print ("An error occurred when inserting into latest table: ", err)
        test.data()

url="https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=7ad82bb68a98a4a16979023ed867b6501b108e6e"
call_api(url)
data = call_api(url)
json_parsed=write_file(data)
csv_write(json_parsed)
engine=connect()
create_table(engine)
test=json_data()
test.dynamic()
test.delete_latest()
test.latest()

#https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_sql.html
