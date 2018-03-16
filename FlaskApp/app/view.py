"""Main module."""
from flask import render_template
from app import app

#app = Flask(__name__)

@app.route('/')
def index():
	returnDict = {}
	returnDict['user'] = 'Amy'
	returnDict['title'] = 'Flask Application'
#	returnDict['info'] = systeminfo.main.main()
	return render_template("index.html", **returnDict)


if __name__ == '__main__':
	app.run(debug=True)
