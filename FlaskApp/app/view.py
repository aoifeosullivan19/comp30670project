"""Main module."""
from flask import render_template
from app import app
from app.dbcon import Examp, Dynamic

#app = Flask(__name__)

@app.route('/')
def index():
	rows = Examp.query.all()
	dynamic = Dynamic.query.all()
	return render_template("index.html", rows=rows, dynamic = dynamic)


if __name__ == '__main__':
	app.run(debug=True)
