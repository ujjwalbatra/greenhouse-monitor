from database import greenhouse_monitor_database
import matplotlib.pyplot as matplotlib_obj
import logging
from datetime import datetime
import random
import leather


# logging.basicConfig(filename="logs/analytics.log", filemode='a', level=logging.DEBUG)


class Analytics(object):
    __raw_data = None
    __formatted_temperature = None
    __formatted_humidity = None

    def __init__(self):
        self.__get_data_from_db()
        self.__format_data()

    def __get_data_from_db(self):
        db_conn = greenhouse_monitor_database.GreenhouseMonitorDatabase()
        self.__raw_data = db_conn.get_all_sensor_data()
        db_conn.close_connection()

    def __format_data(self):
        temperature = []
        humidity = []

        for row in self.__raw_data:
            temp_db = row[2]
            humidity_db = row[3]

            # rounding off temp/humidity to 2 places after the decimal
            temperature.append(int(temp_db))
            humidity.append(int(humidity_db))

        self.__formatted_temperature = temperature
        self.__formatted_humidity = humidity

    def generate_scatter_plot(self):
        boxplot_data = [self.__formatted_temperature, self.__formatted_humidity]
        matplotlib_obj.boxplot(boxplot_data, notch=True)

        # setting labels and title
        matplotlib_obj.title("Distribution in Temprature and Humidity")
        matplotlib_obj.savefig('box_plot.png')

    # used for coloring the graph
    def colorizer(self, d):
        return 'rgb(%i, %i, %i)' % (d.x, d.y, 150)

    def generate_box_plot(self):
        # insert data
        dot_data = [(self.__formatted_temperature[i], self.__formatted_humidity[i]) for i in
                    range(self.__formatted_temperature.__len__())]

        chart = leather.Chart('Humidity vs Temperature (Humidity %rH on y axis & Temperature *c on x axis)')
        chart.add_dots(dot_data, fill_color=self.colorizer)
        chart.to_svg('scatter_plot.svg')


if __name__ == "__main__":
    # try:
    analyse = Analytics()
    analyse.generate_scatter_plot()
    analyse.generate_box_plot()
    # except Exception as e:
    #     logging.warning(e.__str__() + " " + datetime.now().__str__())
