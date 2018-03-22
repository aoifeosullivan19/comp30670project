from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dublinbikesadmin:dublinbikes2018@dublinbikes.cglcinwmtg3w.eu-west-1.rds.amazonaws.com/dublinbikes'
db = SQLAlchemy(app)

class Examp(db.Model):
	__tablename__ = 'static_info'
	id = db.Column('number', db.Integer, primary_key=True)
	location = db.Column('name', db.Unicode)
	lat = db.Column('latitude', db.Float)
	long = db.Column('longitude', db.Float)
	stand = db.Column('bike_stands', db.Integer)

test = Examp.query.all()

#https://www.youtube.com/watch?v=Tu4vRU4lt6k

