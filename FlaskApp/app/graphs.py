import pymysql

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