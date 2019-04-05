from database import greenhouse_monitor_database
from bokeh.plotting import figure, output_file, show
from bokeh.models import Title
from bokeh.io import export_png

import logging
from decimal import Decimal


# logging.basicConfig(filename="/home/pi/greenhouse_monitor/logs/analytics.log", filemode='a', level=logging.DEBUG)


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

            temperature.append(round(temp_db, 2))
            humidity.append(round(humidity_db, 2))

        self.__formatted_temperature = temperature
        self.__formatted_humidity = humidity

    def __generate_scatter_plot(self):
        plot = figure(plot_width=1200, plot_height=1200)

        # format main title
        plot.title.text = "Temperature vs Humidity"
        plot.title.text_color = "black"
        plot.title.text_font_size = "28px"

        # add extra titles
        plot.add_layout(Title(text="Humidity (%rH)", align="center"), "left")
        plot.add_layout(Title(text="Temperature (*c)", align="center"), "below")

        # add a circle renderer with a size, color, and alpha
        plot.circle(self.__formatted_temperature, self.__formatted_humidity, size=8, color="navy", alpha=0.5)

        export_png(plot, filename="scatter_plot.png")

    def generate_graph(self):
        self.__get_data_from_db()
        self.__format_data()
        self.__generate_scatter_plot()


if __name__ == "__main__":
    analyse = Analytics()
    analyse.generate_graph()
