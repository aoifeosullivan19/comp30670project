"""Main module."""
from flask import render_template
from app import app
from app.dbcon import Examp
from app.graphs2 import test
import pygal

# app.graphs2.getgraph()
#app = Flask(__name__)

@app.route('/')
def index():
    result = test.fetchall()
    number = []
    bikes = []
    for x in result:
        number.append(int(x[0]))
        bikes.append(int(x[1]))
    graph = pygal.Line()
    graph.title = 'Testing graph from DB.'
    graph.x_labels = ['label1','label2','label3','label4','label5','label6']
    graph.add('bikes', number)
    graph.add('bikes', bikes)
    graph_data = graph.render_data_uri()
    rows = Examp.query.all()
    return render_template("index.html", rows=rows, graph_data=graph_data)



# @app.route('/pygalexample/')
# def pygalexample():
    # for x in result:
    #     number.append(x[0])
    #     bikes.append(x[1])
    #
    # try:
    #     graph = pygal.Line()
    #     graph.title = 'Testing graph from DB.'
    #     graph.x_labels = ['label1','label2','label3','label4','label5','label6']
    #     graph.add('bikes', [1, 2, 3, 4, 5, 6, 7])
    #     graph.add('bike_stands', [22, 55, 75, 79, 34, 35])
    #     graph_data = graph.render_data_uri()
    #     return render_template("graphing.html", graph_data=graph_data)
    # except Exception as e:
    #     return(e)

if __name__ == '__main__':
	app.run(debug=True)


