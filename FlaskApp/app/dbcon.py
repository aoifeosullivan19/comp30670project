from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Amylouise94:Meninblack1@dbinstance.cjy2yzz9jf0m.us-west-2.rds.amazonaws.com/DummyDB'
db = SQLAlchemy(app)

class Examp(db.Model):
        __tablename__ = 'DummyTable'
        id = db.Column('stationNO', db.Integer, primary_key=True)
        data = db.Column('location', db.Unicode)

test = Examp.query.all()
locations = ""
for ex in test:
	locations += ex.data
	locations += " "
print(locations)

#https://www.youtube.com/watch?v=Tu4vRU4lt6k

