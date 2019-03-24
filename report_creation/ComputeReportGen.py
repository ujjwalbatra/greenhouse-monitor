import csv
class ComputeReportGen:

    def __init__(self,range,rows):
        self.Range=range
        self.Rows=rows
        self.generateReport(self.Range,self.Rows)
    
    def generateReport(self,Range,Rows):
        StartDate=self.getFirstDate(Rows)
        print (StartDate)

        self.checkTemperature(StartDate,Range,Rows)
        self.checkHumidity(StartDate,Range,Rows)

    def getFirstDate(self,rows):
        for row in rows:
            return row[1]
    
    def checkHumidity(self,StartDate,Range,Rows):
        line =	{
            "Date": 0,
            "Status": "OK",
            "Min_diff": 0,
            "Max_diff":0
        }

        for row in Rows:
            if StartDate == row[1]:
                line["Date"]=row[1]
                if(row[2]<Range["min_humidity"]):
                    diff=Range["min_humidity"]-row[2]
                    if(diff>line["Min_diff"]):
                        line["Min_diff"]=diff
                        line["Status"]=("Bad: %d below minimum humidity" %diff)
                if(row[2]>Range["max_humidity"]):
                    diff=row[2]-Range["max_humidity"]
                    if(diff>line["Max_diff"]):
                        line["Max_diff"]=diff
                        line["Status"]=("Bad: %d above maximun humidity" %diff)
            else:
                print(line)
                self.writeCSV(line)
                StartDate=(row[1])
                line["Max_diff"]=0
                line["Min_diff"]=0
                line["Status"]="OK"
            print(line)
        

    
    def checkTemperature(self,StartDate,Range,Rows):
        line =	{
            "Date": 0,
            "Status": "OK",
            "Min_diff": 0,
            "Max_diff":0
        }

        for row in Rows:
            if StartDate == row[1]:
                line["Date"]=row[1]
                if(row[2]<Range["min_temperature"]):
                    diff=Range["min_temperature"]-row[2]
                    if(diff>line["Min_diff"]):
                        line["Min_diff"]=diff
                        line["Status"]=("Bad: %d below minimum temperature" %diff)
                if(row[2]>Range["max_temperature"]):
                    diff=row[2]-Range["max_temperature"]
                    if(diff>line["Max_diff"]):
                        line["Max_diff"]=diff
                        line["Status"]=("Bad: %d above maximun temperature" %diff)
            else:
                print(line)
                self.writeCSV(line)
                StartDate=(row[1])
                line["Max_diff"]=0
                line["Min_diff"]=0
                line["Status"]="OK"
            print(line)
    
    def writeCSV(self,str):
        row = [("%d"%str["Date"]), str["Status"]]
        with open('report.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
            csvFile.close() 