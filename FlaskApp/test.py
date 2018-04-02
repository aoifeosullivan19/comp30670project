from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.dbcon import Examp

engine = create_engine('mysql+mysqldb://dublinbikesadmin:dublinbikes2018@dublinbikes.cglcinwmtg3w.eu-west-1.rds.amazonaws.com/dublinbikes')

Session = sessionmaker(bind=engine, autocommit=True)
session = Session()

sql = session.query(Examp.lat)

print('Queried')

print(sql)

for i in sql:
	print(i)
print('Done')

session.close()
