from sqlalchemy import create_engine
import pandas as pd

conn_str = "mysql+pymysql://dublinbikesadmin:dublinbikes2018@dublinbikes.cglcinwmtg3w.eu-west-1.rds.amazonaws.com/dublinbikes"

conn = create_engine(conn_str)

query = """
 SELECT * from dynamic_info
"""
df = pd.read_sql_query(con=conn, sql=query)

print(df.shape)

df['last_update'] = pd.to_datetime(df['last_update'])
df['day'] = df['last_update'].dt.weekday_name
df['hour'] = df['last_update'].dt.hour
print(df.head())
