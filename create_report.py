from database import greenhouse_monitor_database
import csv
from report_creation import ComputeReportGen
import json

class Report:

    
    
    

    def __init__(self):
        row = ["Date","Status"]
        with open('report.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
            csvFile.close() 
    
    def testValuesDB(self,db):
        db.insert_sensor_data(25,35)
        db.insert_sensor_data(16,35)
        db.insert_sensor_data(17,35)
        db.insert_sensor_data(26,36)
        db.insert_sensor_data(44,36)
        db.insert_sensor_data(28,36)
        db.insert_sensor_data(46,37)
        db.insert_sensor_data(24,37)
        db.insert_sensor_data(28,37)

    def getRange(self):
        with open('config.json') as json_file:  
            data = json.load(json_file)
            print(data['data_range'])
            return data['data_range'] 
    
    def main(self):
        db = greenhouse_monitor_database.GreenhouseMonitorDatabase()
        db.create_tables()
        self.testValuesDB(db)
        range=self.getRange()
        rows=db.query_to_db()
        
        ComputeReportGen.ComputeReportGen(range,rows)

if __name__ == "__main__":
    objName = Report()
    objName.main()