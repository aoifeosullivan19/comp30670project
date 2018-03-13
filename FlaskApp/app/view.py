"""Main module."""
from flask import render_template
from app import app
import systeminfo.main
#from Test import *

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/')
def index():
	returnDict = {}
	returnDict['user'] = 'Amy'
	returnDict['title'] = 'Flask Application'
	#returnDict['info'] = systeminfo.main.main()
	#returnDict['test'] = Test.variable
	return render_template("index.html", **returnDict)


