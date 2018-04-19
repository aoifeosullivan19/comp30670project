import pytest
import sys
import json
import requests
import os.path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect

engine = create_engine('mysql+pymysql://dublinbikesadmin:dublinbikes2018@dublinbikes.cglcinwmtg3w.eu-west-1.rds.amazonaws.com/dublinbikes')
port=3306
connection = engine.connect()
Session = sessionmaker(bind=engine, autocommit=True)
session=Session()

sys.path.append('.')

def test_status():
    """function to test that response from api"""

    url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=7ad82bb68a98a4a16979023ed867b6501b108e6e"
    result = requests.get(url)
    assert result.status_code == 200

def test_fileExists():
    """function to test that csv file has been created"""

    assert os.path.exists("/home/ubuntu/comp30670project/comp30670project/scraper_files/backup.csv")

def test_table():
    """function to test connection to database"""

    Session.configure(bind=engine)
    assert connection
        
def test_Tables():
    """function to check tables exist"""

    connection=engine.connect()
    inspector=inspect(engine)
    assert (len(inspector.get_table_names())) == 7 