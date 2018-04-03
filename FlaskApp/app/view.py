"""Main module."""
from flask import render_template, jsonify, request
from app import app
from app.dbcon import Examp, Dynamic, latest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pygal

engine = create_engine('mysql+pymysql://dublinbikesadmin:dublinbikes2018@dublinbikes.cglcinwmtg3w.eu-west-1.rds.amazonaws.com/dublinbikes')

Session = sessionmaker(bind=engine, autocommit=True)
session = Session()

@app.route('/')
def index():

	return render_template("index.html")

@app.route('/station_info')
def station_info():
	try:
		info = session.query(Examp.location, Examp.lat, Examp.long, Examp.id, Examp.stand)
		arr = []
		for i in info:
			arr.append(i)
		return jsonify(result = arr)
	except Exception as e:
		return str(e)

@app.route('/station_occupancy')
def station_occupancy():
	try:
		id = request.args.get('id')
		sql = session.query(latest.bikes, latest.stands).filter(latest.id == id)
		arr = []
		print(sql)
		for i in sql:
			arr.append(i[0])
			arr.append(i[1])
		print(arr)
		return jsonify(occupancy = arr)
	except Exception as e:
		return str(e)

if __name__ == '__main__':
	app.run(debug=True)

