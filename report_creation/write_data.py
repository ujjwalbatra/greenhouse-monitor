import csv


class WriteData:

    def __init__(self, range_, rows):
        self.__range = range_
        self.__rows = rows

    def generate_report(self):
        start_date = self.__get_first_date(self.__rows)
        self.__check_humidity_temperature(start_date, self.__range, self.__rows)

    # gets the first date to start looping through all the rows in the db .
    def __get_first_date(self, rows):
        for row in rows:
            return row[1]

    # checks the humidity and delivers appropriate message to be written in the csv file
    def __check_humidity_temperature(self, start_date, range_, rows):

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

                if row[3] > range_["max_humidity"]:
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
                self.__write_csv(date, line)
                start_date = (row[1])
                line["Max_humidity_diff"] = 0
                line["Min_temp_diff"] = 0
                line["Max_temp_diff"] = 0
                line["Min_humidity_diff"] = 0

            # write the last row
            if rows[-1] == row:
                self.__write_csv(date, line)

    # Writes a single row to the csv file
    def __write_csv(self, date, line):

        status = "OK"
        reasons = []
        if line["Min_temp_diff"] != 0:
            status = "Bad"
            reasons.append("%.2f less than the minimum temperature. " % float(line["Min_temp_diff"]))
        if line["Max_temp_diff"] != 0:
            status = "Bad"
            reasons.append("%.2f more than the maximum temperature. " % float(line["Max_temp_diff"]))
        if line["Min_humidity_diff"] != 0:
            status = "Bad"
            reasons.append("%.2f less than the minimum humidity. " % float(line["Min_humidity_diff"]))
        if line["Max_humidity_diff"] != 0:
            status = "Bad"
            reasons.append("%.2f less than the maximum humidity. " % float(line["Max_humidity_diff"]))

        reason = ''.join(reasons)

        row = date, status, reason
        with open('report.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
            csvFile.close()
