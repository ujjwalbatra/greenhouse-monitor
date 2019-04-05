from database import greenhouse_monitor_database
import matplotlib.pyplot as plt

import logging
from decimal import Decimal

logging.basicConfig(filename="logs/analytics.log", filemode='a', level=logging.DEBUG)


class Analytics(object):
    __raw_data = None
    __formatted_temperature = None
    __formatted_humidity = None

    def __get_data_from_db(self):
        db_conn = greenhouse_monitor_database.GreenhouseMonitorDatabase()
        self.__raw_data = db_conn.get_all_sensor_data()
        db_conn.close_connection()

    def __format_data(self):
        temperature = []
        humidity = []

        for row in self.__raw_data:
            temp_db = Decimal(row[2])
            humidity_db = Decimal(row[3])

            # rounding off temp/humidity to 2 places after the decimal
            temperature.append(round(temp_db, 2))
            humidity.append(round(humidity_db, 2))

        self.__formatted_temperature = temperature
        self.__formatted_humidity = humidity

    def __generate_scatter_plot(self):
        plt.scatter(self.__formatted_temperature, self.__formatted_humidity, 8, "navy", alpha=0.5)

        # setting labels and title
        plt.xlabel("Temprature (*c)")
        plt.ylabel("Humidity (%rH)")
        plt.title("Temperature vs Humidity")

        plt.savefig('scatter_plot.png')

    def generate_graph(self):
        self.__get_data_from_db()
        self.__format_data()
        self.__generate_scatter_plot()


if __name__ == "__main__":
    try:
        analyse = Analytics()
        analyse.generate_graph()
    except Exception as e:
        logging.warning(e.__str__() + " " + datetime.now().__str__())
