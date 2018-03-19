import requests
import json
import csv
import time
import schedule
import sched

def data_collector (url):
    """Retrieves information from Dublin Bikes API and stores as JSON"""
    
    req = requests.get(url)
    req_text= req.text
    json_parsed=json.loads(req_text)
    return json_parsed

def write_to_csv(filename):
    """Converts parsed json to csv and stores in csv file"""

    csv_data=filename[0:]
    csv1_data = open('data190318.csv', 'a')
    csvwriter = csv.writer(csv1_data)
    count = 0
    
    for i in csv_data:
        if count == 0:
            header = i.keys()
            csvwriter.writerow(header)
            count += 1
        csvwriter.writerow(i.values())
    csv1_data.close()
    return()
      

def job():
    """Runs the convert to csv function"""
    
    url="https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=7ad82bb68a98a4a16979023ed867b6501b108e6e"
    while True:
        filename=data_collector(url)
        time.sleep(300)
        filename=data_collector(url)
        write_to_csv(filename)



url="https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=7ad82bb68a98a4a16979023ed867b6501b108e6e"
filename=data_collector(url)

job()

