from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Amylouise94:Meninblack1@dummydb.cbsshlsxbajt.us-west-2.rds.amazonaws.com/DummyDB'
db = SQLAlchemy(app)

class Examp(db.Model):
	__tablename__ = 'DummyTable'
	id = db.Column('stationNO', db.Integer, primary_key=True)
	location = db.Column('location', db.Unicode)
	lat = db.Column('lat', db.Float)
	long = db.Column('longi', db.Float)

test = Examp.query.all()

#https://www.youtube.com/watch?v=Tu4vRU4lt6k