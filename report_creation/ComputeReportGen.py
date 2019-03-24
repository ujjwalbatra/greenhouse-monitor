import csv


class ComputeReportGen:

    def __init__(self, range_, rows):
        self.range_ = range_
        self.rows = rows
        self.generate_report(self.range_, self.rows)
    
    def generate_report(self, range_, rows):
        start_date = self.get_first_date(rows)
        print(start_date)

        self.check_temperature(start_date, range_, rows)
        self.check_humidity(start_date, range_, rows)

    # gets the first date to start looping through all the rows in the db .
    def get_first_date(self, rows):
        for row in rows:
            return row[1]

    # checks the humidity and delivers appropriate message to be written in the csv file
    def check_humidity(self, start_date, range_, rows):
        line ={
            "Date": 0,
            "Status": "OK",
            "Min_diff": 0,
            "Max_diff": 0
        }

        for row in rows:
            if start_date == row[1]:
                line["Date"] = row[1]
                if row[2] < range_["min_humidity"] :
                    diff = range_["min_humidity"] - row[2]
                    if diff > line["Min_diff"]:
                        line["Min_diff"] = diff
                        line["Status"] = ("Bad: %d below minimum humidity" % diff)
                if row[2] > range_["max_humidity"] :
                    diff = row[2] - range_["max_humidity"]
                    if diff > line["Max_diff"]:
                        line["Max_diff"] = diff
                        line["Status"] = ("Bad: %d above maximum humidity" % diff)
            else:
                print(line)
                self.write_csv(line)
                start_date=(row[1])
                line["Max_diff"]=0
                line["Min_diff"]=0
                line["Status"]="OK"
            print(line)

    # checks the Temperature and delivers appropriate message to be written in the csv file
    def check_temperature(self, start_date, range_, rows):
        line ={
            "Date": 0,
            "Status": "OK",
            "Min_diff": 0,
            "Max_diff": 0
        }

        for row in rows:
            if start_date == row[1]:
                line["Date"]=row[1]
                if row[2] < range_["min_temperature"]:
                    diff = range_["min_temperature"] - row[2]
                    if diff > line["Min_diff"]:
                        line["Min_diff"] = diff
                        line["Status"] = ("Bad: %d below minimum temperature" % diff)
                if row[2] > range_["max_temperature"] :
                    diff = row[2] - range_["max_temperature"]
                    if diff > line["Max_diff"]:
                        line["Max_diff"]=diff
                        line["Status"]=("Bad: %d above maximum temperature" %diff)
            else:
                print(line)
                self.write_csv(line)
                start_date=(row[1])
                line["Max_diff"]=0
                line["Min_diff"]=0
                line["Status"]="OK"
            print(line)

    # Writes a single row to the csv file
    def write_csv(self, line):
        row = [("%d" % line ["Date"] ), line["Status"]]
        with open('report.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
            csvFile.close()
