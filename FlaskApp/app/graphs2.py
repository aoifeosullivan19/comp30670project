import pymysql
import pandas as pd
#%matplotlib inline
import matplotlib.pyplot as plt
import pygal


host = "dublinbikes.cglcinwmtg3w.eu-west-1.rds.amazonaws.com"
port = 3306
dbname = "dublinbikes"
user = "dublinbikesadmin"
password = "dublinbikes2018"
try:
    print("Connecting to SQL")
    conn = pymysql.connect(host, user=user,port=port,
                           passwd=password, db=dbname)
    test = conn.cursor()
    test.execute("select number, bike_stands from static_info;")
    print("Connection successful")
except Exception as e:
    print("Oops...unable to connect to database at present")
    print(e)

# result = test.fetchall()
#
# number = []
# bikes = []

# for x in result:
#     number.append(x[0])
#     bikes.append(x[1])

# def pygalexample():
    # for x in result:
    #     number.append(x[0])
    #     bikes.append(x[1])
    #
    # try:
    #     graph = pygal.Line()
    #     graph.title = 'Testing graph from DB.'
    #     graph.x_labels = ['label1','label2','label3','label4','label5','label6']
    #     graph.add('bikes', bikes)
    #     graph.add('bike_stands', number)
    #     graph_data = graph.render_data_uri()
    #     return render_template("graphing.html", graph_data = graph_data)
    # except Exception as e:
    #     return(e)

# plt.plot(number, bikes)
# plt.show()



#references
#https://www.youtube.com/watch?v=UX1DAlG5YnQ
#https://pythonprogramming.net/pygal-tutorial/ -- using pygal to graph data




# def getgraph():
#     host = "dublinbikes.cglcinwmtg3w.eu-west-1.rds.amazonaws.com"
#     port = 3306
#     dbname = "dublinbikes"
#     user = "dublinbikesadmin"
#     password = "dublinbikes2018"
#     try:
#         print("Connecting to SQL")
#         conn = pymysql.connect(host, user=user,port=port,
#                                passwd=password, db=dbname)
#         test = conn.cursor()
#         test.execute("select name, bike_stands from static_info;")
#         print("Connection successful")
#     except Exception as e:
#         print("Oops...unable to connect to database at present")
#         print(e)
#
#     result = test.fetchall()
#     return result

