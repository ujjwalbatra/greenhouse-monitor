import csv


class WriteData:

    def __init__(self, range_, rows, file):
        self.__range = range_
        self.__rows = rows
        self.csvFile = file

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
            "min_temp_diff": 0,
            "max_temp_diff": 0,
            "min_humidity_diff": 0,
            "max_humidity_diff": 0,
        }

        time_of_occurance = {
            "min_temp_time": None,
            "max_temp_time": None,
            "min_humidity_time": None,
            "max_humidity_time": None,
        }

        date = start_date

        for row in rows:
            if start_date == row[1]:
                date = row[1]
                if row[3] < range_["min_humidity"]:
                    diff = range_["min_humidity"] - row[2]
                    if diff > line["min_humidity_diff"]:
                        line["min_humidity_diff"] = diff
                        time_of_occurance["min_humidity_time"] = row[4]

                if row[3] > range_["max_humidity"]:
                    diff = row[3] - range_["max_humidity"]
                    if diff > line["max_humidity_diff"]:
                        line["max_humidity_diff"] = diff
                        time_of_occurance["max_humidity_time"] = row[4]

                if row[2] < range_["min_temperature"]:
                    diff = range_["min_temperature"] - row[2]
                    if diff > line["min_temp_diff"]:
                        line["min_temp_diff"] = diff
                        time_of_occurance["min_temp_time"] = row[4]

                if row[2] > range_["max_temperature"]:
                    diff = row[2] - range_["max_temperature"]
                    if diff > line["max_temp_diff"]:
                        line["max_temp_diff"] = diff
                        time_of_occurance["max_temp_time"] = row[4]

            else:
                self.__write_csv(date, line, time_of_occurance)
                start_date = (row[1])
                line["max_humidity_diff"] = 0
                line["min_temp_diff"] = 0
                line["max_temp_diff"] = 0
                line["min_humidity_diff"] = 0
                time_of_occurance["min_humidity_time"] = None
                time_of_occurance["max_temp_time"] = None
                time_of_occurance["min_temp_time"] = None
                time_of_occurance["max_humidity_time"] = None

            # write the last row
            if rows[-1] == row:
                self.__write_csv(date, line, time_of_occurance)

    # Writes a single row to the csv file
    def __write_csv(self, date, line, time_of_occurance):

        status = "OK"
        reasons = []
        if line["min_temp_diff"] != 0:
            status = "Bad"
            min_temp_time = time_of_occurance["min_temp_time"]
            reasons.append("%.2f less than the minimum temperature at %s. " %
                           (float(line["min_temp_diff"]), min_temp_time))
        if line["max_temp_diff"] != 0:
            status = "Bad"
            max_temp_time = time_of_occurance["max_temp_time"]
            reasons.append("%.2f more than the maximum temperature at %s. " %
                           (float(line["max_temp_diff"]), max_temp_time))
        if line["min_humidity_diff"] != 0:
            status = "Bad"
            min_humidity_time = time_of_occurance["min_humidity_time"]
            reasons.append("%.2f less than the minimum humidity at %s. " %
                           (float(line["min_humidity_diff"]), min_humidity_time))
        if line["max_humidity_diff"] != 0:
            status = "Bad"
            max_humidity_time = time_of_occurance["max_humidity_time"]
            reasons.append("%.2f less than the maximum humidity at %s. " %
                           (float(line["max_humidity_diff"]), max_humidity_time))

        reason = ''.join(reasons)

        row = date, status, reason
        with open(self.csvFile, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
            csvFile.close()
