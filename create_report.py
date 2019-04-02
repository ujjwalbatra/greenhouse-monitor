from database import greenhouse_monitor_database
import csv
from report_creation import write_data
import json


class CreateReport:
    __range = None

    # initializes the report
    def __initialize_headers(self):
        row = ["Date", "Status", "Reason"]
        with open('report.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
            csvFile.close()

    # gets the range of temperature and humidity to compare
    def get_range(self):
        with open('config.json') as json_file:
            data = json.load(json_file)
            return data['data_range']

    def main(self):
        # make csv file with headers
        self.__initialize_headers()

        # get all sensors data
        db = greenhouse_monitor_database.GreenhouseMonitorDatabase()
        self.__range = self.get_range()
        rows = db.get_all_sensor_data()

        # write data tro csv
        write_data_ = write_data.WriteData(self.__range, rows)
        write_data_.generate_report()


if __name__ == "__main__":
    objName = CreateReport()
    objName.main()
