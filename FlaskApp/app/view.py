"""Main module."""
from collections import defaultdict, OrderedDict
from flask import render_template, jsonify, request
from app import app
from app.dbcon import Examp, Dynamic, latest, weather, weather_predictions
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
import pygal
import pandas as pd
import datetime
import time
import json
import pickle

engine = create_engine('mysql+pymysql://dublinbikesadmin:dublinbikes2018@dublinbikes.cglcinwmtg3w.eu-west-1.rds.amazonaws.com/dublinbikes')

Session = sessionmaker(bind=engine, autocommit=True)
session = Session()

@app.route('/')
def index():

	return render_template("index.html")

@app.route('/station_info')
def station_info():
	try:
		info = session.query(Examp.location, Examp.lat, Examp.long, Examp.id)
		info2 = session.query(latest.bikes, latest.id)

		arr1 = []
		for j in info2:
			arr1.append(j)
		arr = []
		for i in info:
			arr.append(i)

		return jsonify(result = arr, bikeres = arr1)
	except Exception as e:
		return str(e)

@app.route('/station')
def station():
	try:
		info = session.query(Examp.location, Examp.lat, Examp.long, Examp.id)
		stations = []

		for arr in info:
			stations.append(dict(arr))
		return jsonify(stations=stations)

	except Exception as e:
		return str(e)    

@app.route('/station_occupancy')
def station_occupancy():
	try:
		id = request.args.get('id')
		sql = session.query(latest.bikes, latest.stands).filter(latest.id == id)
		arr = []

		for i in sql:
			arr.append(i[0])
			arr.append(i[1])

		return jsonify(occupancy = arr)
	except Exception as e:
		return str(e)

@app.route('/occupancy')
def occupancy():
	try:
		id = request.args.get('id')

		sql = session.query(latest.bikes, latest.stands).filter(latest.id == id)
		arr = []
		for i in sql:
			arr.append(i[0])
			arr.append(i[1])

		return jsonify(occupancy = arr)
	except Exception as e:
		return str(e)


@app.route('/current_weather')
def current_weather():
	try:
		info = session.query(weather.temp, weather.temp_min, weather.temp_max, weather.description, weather.mainDescription, weather.speed, weather.deg, weather.dt_txt, weather.humidity, weather.rain)
		arr = [];
		for i in info:
			arr.append(i)
		return jsonify(current = arr)
	except Exception as e:
		return str(e)

@app.route('/graph_info')
def graph_info():
	try:
		id = request.args.get('id')
		conn_str = "mysql+pymysql://dublinbikesadmin:dublinbikes2018@dublinbikes.cglcinwmtg3w.eu-west-1.rds.amazonaws.com/dublinbikes"
		conn = create_engine(conn_str)

		query = """
 		SELECT * from bike_dynamic where number = {};
		"""
		df = pd.read_sql_query(con=conn, sql=query.format(id))

		df['last_update'] = pd.to_datetime(df['last_update'])
		df['day'] = df['last_update'].dt.weekday_name
		df['hour'] = df['last_update'].dt.hour

		names = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday','Friday', 'Saturday', 'Sunday']
		df['day'] = df['day'].astype('category', categories=names, ordered=True)

		y = df.groupby(['day','hour'])['available_bikes'].mean()
		y = OrderedDict(y)
		d = defaultdict(list)

		arr = []
		for k,v in y.items():
			if k[0] not in arr:
        			arr.append(k[0])
			d[k[1]].append(v)

		return jsonify(data = d, day = arr)
	except Exception as e:
		return str(e)

@app.route('/weathergraph_info')
def weathergraph_info():
	try:
		req = request.args.get('id')
		req = req.split(',')
		id, weather = req[0], req[1]
		if weather == 'rain':

			file = "app/pickleFiles/stationRain"+id+".pickle"
			pickle_in = open(file,"rb")
			data = pickle.load(pickle_in)
		elif weather == 'sun':
			file = "app/pickleFiles/stationDry"+id+".pickle"
			pickle_in = open(file,"rb")
			data = pickle.load(pickle_in)

		pickle_inDays = open('app/pickleFiles/day.pickle','rb')

		day = pickle.load(pickle_inDays)

		return jsonify(data = data, day = day)

	except Exception as e:
		return str(e)

@app.route('/occupancy_prediction')
def occupancy_prediction():
	try:
		req = request.args.get('id')
		req = req.split(",")
		id, time_req, day = req[0], req[1], req[2]

		now = datetime.datetime.now().date()
		day_num = time.strptime(day, "%A").tm_wday

		date = next_weekday(now, day_num)
		date = str(date)
		date_time = date + " " + time_req + ":00"

		info = session.query(weather_predictions.mainDescription).filter(weather_predictions.dt_txt == date_time).first()
		if info == None:
			arr = []
			sql = session.query(func.avg(latest.bikes)).filter(latest.id == id).scalar()
			arr.append(False)
			arr.append(sql)
			return jsonify(occupancy = arr)
		else:
			info = session.query(weather_predictions.mainDescription).filter(weather_predictions.dt_txt == date_time)
			arr = []
			for i in info:
				arr.append(i)
			weather = arr[0]

			if weather == 'Rain' or weather == 'Drizzle' or weather == 'Fog' or weather == 'Snow':
				file = "app/pickleFiles/stationRain"+id+".pickle"
				pickle_in = open(file,"rb")
				data = pickle.load(pickle_in)
			else:
				file = "app/pickleFiles/stationDry"+id+".pickle"
				pickle_in = open(file,"rb")
				data = pickle.load(pickle_in)

				pred_time = int(time_req[:-3])

				prediction = data[pred_time][day_num]
				prediction = int(prediction)
				arr.append(prediction)

		return jsonify(occupancy = arr)
	except Exception as e:
		return str(e)

def next_weekday(d, weekday):
	days_ahead = weekday - d.weekday()
	if days_ahead <= 0:
		days_ahead += 7
	return d + datetime.timedelta(days_ahead)



if __name__ == '__main__':
	app.run(debug=True)

