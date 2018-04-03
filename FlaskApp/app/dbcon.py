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


#https://www.youtube.com/watch?v=Tu4vRU4lt6k
