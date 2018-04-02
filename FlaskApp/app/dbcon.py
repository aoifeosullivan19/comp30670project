from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Float, Unicode
from sqlalchemy.ext.declarative import declarative_base
import pymysql

#app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dublinbikesadmin:dublinbikes2018@dublinbikes.cglcinwmtg3w.eu-west-1.rds.amazonaws.com/dublinbikes'
#db = SQLAlchemy(app)
Base = declarative_base()

class Examp(Base):
	__tablename__ = 'static_info'
	id = Column('number', Integer, primary_key=True)
	location =Column('name', Unicode)
	lat = Column('latitude', Float)
	long = Column('longitude', Float)
	stand = Column('bike_stands', Integer)

class Dynamic(Base):
	__tablename__ = 'dynamic_info'
	id = Column('number', Integer, primary_key=True)
	bikes = Column('available_bikes', Integer)
	stands = Column('available_bike_stands', Integer)
#	time = Column('last_update', db.DateTime)

#test = Examp.query.all()
#test_dynam = Dynamic.query.all()
#https://www.youtube.com/watch?v=Tu4vRU4lt6k
