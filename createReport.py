from database import greenhouse_monitor_database

import csv

row = ["Date","Status"]
with open('report.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(row)
    csvFile.close()
db = greenhouse_monitor_database.GreenhouseMonitorDatabase()

db.insert_to_db(25,35)
db.insert_to_db(16,35)
db.insert_to_db(17,35)
db.insert_to_db(26,36)
db.insert_to_db(44,36)
db.insert_to_db(28,36)
db.insert_to_db(46,37)
db.insert_to_db(24,37)
db.insert_to_db(28,37)


line =	{
  "Date": 0,
  "Status": "OK",
  "Min_diff": 0,
  "Max_diff":0
}
import json

def getMinMax():
    with open('config.json') as json_file:  
        data = json.load(json_file)
        print(data['data_range'])
        return data['data_range']        











def writecsv(str):
    row = [("%d"%str["Date"]), str["Status"]]
    with open('report.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
        csvFile.close()
    

_=35
rows=db.query_to_db()
x=getMinMax()
for row in rows:
   
    if _ == row[3]:
        line["Date"]=row[3]
        if(row[2]<x["min_temperature"]):
           diff=x["min_temperature"]-row[2]
           if(diff>line["Min_diff"]):
                line["Min_diff"]=diff
                line["Status"]=("Bad: %d below minimum " %diff)
        if(row[2]>x["max_temperature"]):
           diff=row[2]-x["max_temperature"]
           if(diff>line["Max_diff"]):
                line["Max_diff"]=diff
                line["Status"]=("Bad: %d above maximun " %diff)
    else:
        print(line)
        writecsv(line)
        _=(row[3])
        line["Max_diff"]=0
        line["Min_diff"]=0
        line["Status"]="OK"



