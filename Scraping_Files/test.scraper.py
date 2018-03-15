import requests
import json
import csv

url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=7ad82bb68a98a4a16979023ed867b6501b108e6e"
req = requests.get(url)
req_text= req.text
json_parsed=json.loads(req_text)
csv_data=json_parsed[0:]
csv1_data = open('test.csv', 'a')

csvwriter = csv.writer(csv1_data)

count = 0

for i in csv_data:

      if count == 0:

             header = i.keys()

             csvwriter.writerow(header)

             count += 1

      csvwriter.writerow(i.values())

csv1_data.close()

