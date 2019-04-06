from database import greenhouse_monitor_database
import matplotlib.pyplot as matplotlib_obj
import pandas
import seaborn
import logging


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
            temp_db = int(row[2])
            humidity_db = int(row[3])

            # rounding off temp/humidity to 2 places after the decimal
            temperature.append(round(temp_db, 2))
            humidity.append(round(humidity_db, 2))

        self.__formatted_temperature = temperature
        self.__formatted_humidity = humidity

    def generate_scatter_plot(self):
        matplotlib_obj.scatter(self.__formatted_temperature, self.__formatted_humidity, 8, "navy", alpha=0.5)

        # setting labels and title
        matplotlib_obj.xlabel("Temprature (*c)")
        matplotlib_obj.ylabel("Humidity (%rH)")
        matplotlib_obj.title("Temperature vs Humidity")

        matplotlib_obj.savefig('scatter_plot.png')

    def generate_boxplot(self):
        sensor_data_dict = {'temperature': self.__formatted_temperature, 'humidity': self.__formatted_humidity}

        dataframe = pandas.DataFrame().from_dict(sensor_data_dict)

        seaborn_plot = seaborn.boxplot(data=dataframe, width=0.5).set_title('Distribution in Temprature and Humidity')
        matplotlib_obj.xlabel("")
        matplotlib_obj.ylabel("")
        image = seaborn_plot.get_figure()
        image.savefig("boxplot.png")


if __name__ == "__main__":
    # try:
    analyse = Analytics()
    analyse.generate_scatter_plot()
    analyse.generate_boxplot()
    # except Exception as e:
    #     logging.warning(e.__str__() + " " + datetime.now().__str__())
