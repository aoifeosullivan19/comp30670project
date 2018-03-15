"""Main module."""
from flask import render_template
from app import app
from app.test import *
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import base64

#print(matplotlib.get_backend())

#plt.plot(range(10))

#plt.savefig('test.png')
#from Test import *


@app.route('/')
def index():
	returnDict = {}
	returnDict['user'] = 'Amy'
	returnDict['title'] = 'Flask Application'
	#returnDict['info'] = systeminfo.main.main()
	return render_template("index.html", **returnDict)


