import csv


class ComputeReportGen:

    def __init__(self, range_, rows):
        self.range_ = range_
        self.rows = rows
        self.generate_report(self.range_, self.rows)
    
    def generate_report(self, range_, rows):
        start_date = self.get_first_date(rows)
        print(start_date)

        self.check_humidity_temperature(start_date, range_, rows)

    # gets the first date to start looping through all the rows in the db .
    def get_first_date(self, rows):
        for row in rows:
            return row[1]

    # checks the humidity and delivers appropriate message to be written in the csv file

    def check_humidity_temperature(self, start_date, range_, rows):

        line = {
            "Min_temp_diff": 0,
            "Max_temp_diff": 0,
            "Min_humidity_diff": 0,
            "Max_humidity_diff": 0
        }
        date = start_date

        for row in rows:
            if start_date == row[1]:
                date = row[1]
                if row[3] < range_["min_humidity"]:
                    diff = range_["min_humidity"] - row[2]
                    if diff > line["Min_humidity_diff"]:
                        line["Min_humidity_diff"] = diff

                if row[3] > range_["max_humidity"] :
                    diff = row[3] - range_["max_humidity"]
                    if diff > line["Max_humidity_diff"]:
                        line["Max_humidity_diff"] = diff

                if row[2] < range_["min_temperature"]:
                    diff = range_["min_temperature"] - row[2]
                    if diff > line["Min_temp_diff"]:
                        line["Min_temp_diff"] = diff

                if row[2] > range_["max_temperature"]:
                    diff = row[2] - range_["max_temperature"]
                    if diff > line["Max_temp_diff"]:
                        line["Max_temp_diff"] = diff

            else:
                self.write_csv(date, line)
                start_date = (row[1])
                line["Max_humidity_diff"] = 0
                line["Min_temp_diff"] = 0
                line["Max_temp_diff"] = 0
                line["Min_humidity_diff"] = 0

            if rows[-1] == row:
                self.write_csv(date, line)

    # Writes a single row to the csv file
    def write_csv(self, date, line):

        status = "OK"
        reasons = []
        if line["Min_temp_diff"] != 0:
            status = "Bad"
            reasons.append("%s less than the minimum temperature" % line["Min_temp_diff"])
        if line["Max_temp_diff"] != 0:
            status = "Bad"
            reasons.append("%s more than the maximum temperature" % line["Max_temp_diff"])
        if line["Min_humidity_diff"] != 0:
            status = "Bad"
            reasons.append("%s less than the minimum humidity" % line["Min_humidity_diff"])
        if line["Max_humidity_diff"] != 0:
            status = "Bad"
            reasons.append("%s less than the maximum humidity" % line["Max_humidity_diff"])

        row = date, status, reasons
        with open('report.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
            csvFile.close()
