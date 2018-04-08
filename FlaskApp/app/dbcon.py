from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Float, Unicode
from sqlalchemy.ext.declarative import declarative_base
import pymysql

Base = declarative_base()

class Examp(Base):
	__tablename__ = 'static_info'
	id = Column('number', Integer, primary_key=True)
	location =Column('address', Unicode)
	lat = Column('latitude', Float)
	long = Column('longitude', Float)
	stand = Column('bike_stands', Integer)

class Dynamic(Base):
	__tablename__ = 'dynamic_info'
	id = Column('number', Integer, primary_key=True)
	bikes = Column('available_bikes', Integer)
	stands = Column('available_bike_stands', Integer)
#	time = Column('last_update', db.DateTime)


class latest(Base):
        __tablename__ = 'latest_info'
        id = Column('number', Integer, primary_key=True)
        bikes = Column('available_bikes', Integer)
        stands = Column('available_bike_stands', Integer)
#       time = Column('last_update', db.DateTime)

class weather(Base):
        __tablename__ = 'dynamic_weather'
        temp = Column('temp', Float)
        temp_min = Column('temp_min', Float)
        temp_max = Column('temp_max', Float)
        description = Column('description', Unicode)
        mainDescription = Column('mainDescription', Unicode)
        speed = Column('speed', Float)
        deg = Column('def', Float)
        dt_txt = Column('dt_txt', Unicode, primary_key=True)
        humidity = Column('humidity', Float)
        rain = Column('rain', Float)


#https://www.youtube.com/watch?v=Tu4vRU4lt6k
