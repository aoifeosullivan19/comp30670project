
"""Main module."""
from collections import defaultdict, OrderedDict
from flask import render_template, jsonify, request
from app import app
from app.dbcon import Examp, Dynamic, latest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pygal
import pandas as pd
import json

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


if __name__ == '__main__':
	app.run(debug=True)

