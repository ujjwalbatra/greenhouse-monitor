from database import greenhouse_monitor_database
import csv
from report_creation import compute_report_gen
import json


class Report:

    # initializes the report
    def __init__(self):
        row = ["Date", "Status", "Reason"]
        with open('report.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
            csvFile.close() 
    
    def test_values_db(self, db):
        db.insert_sensor_data(21, 55)
        db.insert_sensor_data(21, 55)
        db.insert_sensor_data(21, 55)
        db.insert_sensor_data(21, 55)
        db.insert_sensor_data(21, 55)
        db.insert_sensor_data(21, 55)
        db.insert_sensor_data(21, 55)
        db.insert_sensor_data(21, 55)
        db.insert_sensor_data(21, 55)

    # gets the range of temperature and humidity to compare
    def get_range(self):
        with open('config.json') as json_file:  
            data = json.load(json_file)
            return data['data_range'] 
    
    def main(self):
        db = greenhouse_monitor_database.GreenhouseMonitorDatabase()
        db.create_tables()
        self.test_values_db(db)
        range_ = self.get_range()
        rows = db.query_to_db()
        
        compute_report_gen.ComputeReportGen(range_, rows)


if __name__ == "__main__":
    objName = Report()
    objName.main()
