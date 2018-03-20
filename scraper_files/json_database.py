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

#http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
Base = declarative_base()
Session = sessionmaker()
def data_collector (url):
    """Retrieves information from Dublin Bikes API and stores as JSON"""

    req = requests.get(url)
    req_text= req.text
    json_parsed=json.loads(req_text)
    return json_parsed


url="https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=7ad82bb68a98a4a16979023ed867b6501b108e6e"
filename=data_collector(url)


def connect():
    """Function to connect to database on Amazon Web Services"""

    engine = create_engine('mysql+mysqlconnector://dublinbikesadmin:dublinbikes2018@dublinbikes.cglcinwmtg3w.eu-west-1.rds.amazonaws.com/dublinbikes')    
    port=3306
    connection = engine.connect()
    Session.configure(bind=engine)
    #https://campus.datacamp.com/courses/introduction-to-relational-databases-in-python/advanced-sqlalchemy-queries?ex=2#skiponboarding
    
class Tables(Base):
    __tablename__ = 'static_info'

    name=Column(String)
    number=Column(Integer, primary_key=True)
    address=Column(String)
    banking=Column(String)
    stands=Column(String)
    position=Column(String)
    status=Column(String)

    def __repr__(self):
        return "<Tables(name='%s', number='%s', address='%s', banking='%s', stands='%s', position='%s', status='%s')>" % (self.name, self.number, self.address, self.banking, self.stands, self.position, self.status)


def create_table(databasename):
    """Function to create new table in given database"""

    cursor = databasename.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS static_bike (number int(11) NOT NULL PRIMARY KEY, name varchar(125),
        address varchar(135), position varchar(135), banking varchar(135), status varchar(135), bike_stands int(11),  bonus varchar(135), available_bike_stands int(11), available_bikes int(11), contract_name varchar(135), last_update varchar(135))""") 
    databasename.commit()

def insert(databasename):
    """Function to insert values into database table"""

    cursor=databasename.cursor()
    new_dict={}
    new_dict=data_collector(url)
    sql="INSERT INTO static_bike (number, name, address, position, banking, status, bike_stands, bonus, available_bike_stands, available_bikes, contract_name, last_update) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute (sql, (json.dumps(new_dict),))    
    databasename.commit()
    cursor.close()
    databasename.close()
    return

connect()
Base = declarative_base()
test=Tables(name='aoife', number='3', address='34 street', banking='yes', stands='30', position='3 sdf', status='no')
session=Session()
session.add(test)
session.commit()
