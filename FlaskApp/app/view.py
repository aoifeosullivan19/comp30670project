"""Main module."""
from flask import render_template, jsonify
from app import app
from app.dbcon import Examp, Dynamic
from app.graphs2 import test
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pygal

engine = create_engine('mysql+pymysql://dublinbikesadmin:dublinbikes2018@dublinbikes.cglcinwmtg3w.eu-west-1.rds.amazonaws.com/dublinbikes')

Session = sessionmaker(bind=engine, autocommit=True)
session = Session()

@app.route('/')
def index():

	rows  = session.query(Examp)

	#for row in sql:
	#	print(row)
	number = []
	bikes = []

#	for x in result:
#		number.append(int(x[0]))
#		bikes.append(int(x[1]))
#		graph = pygal.Line()
#		graph.title = 'Testing graph from DB.'
#		graph.x_labels = ['label1', 'label2', 'label3', 'label4', 'label5', 'label6']
#		graph.add('bikes', number)
#		graph.add('bikes', bikes)
#	graph_data = graph.render_data_uri()
#	rows = Examp.query.all()

	return render_template("index.html", rows=rows)

@app.route('/station_info')
def station_info():
	try:
		info = session.query(Examp.location, Examp.lat, Examp.long)
		arr = []
		for i in info:
			arr.append(i)
		return jsonify(result = arr)
	except Exception as e:
		return str(e)

if __name__ == '__main__':
	app.run(debug=True)

