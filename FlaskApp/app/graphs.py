import pymysql
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

host = "testdb.cxb1icy6ikcz.us-east-2.rds.amazonaws.com"
port = 3306
dbname = "TestDataBase"
user = "MuireannMacC"
password = "muireannpassword"
try:
    print("Connecting to SQL")
    conn = pymysql.connect(host, user=user,port=port,
                           passwd=password, db=dbname)
    print("Connection successful")
except Exception as e:
    print("Oops...unable to connect to database at present")
    print(e)



pd.read_sql('select * from TestTable;', con=conn)
pandas_df = pd.read_sql('select * from TestTable;', con=conn)
pandas_df.groupby(pandas_df.station).size().plot(kind='bar', ylim=[0, 40])
plt.xlabel('station')
plt.ylabel('bikes')
plt.savefig('Fig1')


pandas_df.plot(kind='scatter', x='station', y='available_bikes')
plt.savefig('Fig2')


pandas_df.plot(kind='line', x='station', y='available_stands')
plt.savefig('Fig3')


#references
#https://github.com/ufoym/deepo/issues/17 (for using agg with matplotlib)
#http://benalexkeen.com/creating-graphs-using-flask-and-d3/ -- try make graphs to flask using pandas