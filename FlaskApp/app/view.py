"""Main module."""
from flask import render_template
from app import app
from app.dbcon import Examp, Dynamic
from app.graphs2 import test
import pygal

#app = Flask(__name__)

@app.route('/')
def index():
	#this code creates a pygal graph from the connection made in graphs2.py and
	#sends it to index html
	#there are different ways to send this graph to flask app
	#I chose in this example to embed it in the html (see index.html)
	rows = Examp.query.all()
	dynamic = Dynamic.query.all()
	result = test.fetchall()
	number = []
	bikes = []

	for x in result:
		number.append(int(x[0]))
		bikes.append(int(x[1]))
		graph = pygal.Line()
		graph.title = 'Testing graph from DB.'
		graph.x_labels = ['label1', 'label2', 'label3', 'label4', 'label5', 'label6']
		graph.add('bikes', number)
		graph.add('bikes', bikes)
	graph_data = graph.render_data_uri()
	rows = Examp.query.all()

	return render_template("index.html", rows=rows, graph_data=graph_data, dynamic=dynamic)



if __name__ == '__main__':
	app.run(debug=True)

