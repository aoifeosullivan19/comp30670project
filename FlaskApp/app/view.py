"""Main module."""
from flask import render_template
from app import app
from app.dbcon import Examp

#app = Flask(__name__)

@app.route('/')
def index():
	row = Examp.query.all()
	return render_template("index.html", rows=rows)


if __name__ == '__main__':
	app.run(debug=True)
