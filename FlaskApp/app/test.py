'''
Created on 13 Mar 2018

@author: HP
'''

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


import matplotlib.patches as mpatches
#import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import io
import base64

df = pd.read_csv("CustomerChurn-12333766.csv", keep_default_na=True, sep=',\s+', delimiter=',', skipinitialspace=True)

int_columns = df.select_dtypes(['int64']).columns


def testing():
    returnDict = {}
    #returnDict['title'] = 'Flask Application'
    #returnDict['user'] = 'Amy'
    img = io.BytesIO()

    y = [1,2,3,4,5]
    x = [0,2,1,3,4]
    plt.plot(x,y)
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()
    return '<img src="data:image/png;base64,{}">'.format(plot_url)

if __name__ == '__main__':
    testing()
