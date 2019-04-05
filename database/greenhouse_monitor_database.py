import sqlite3
import json
from sqlite3 import Error
from datetime import date


class GreenhouseMonitorDatabase(object):

    def __init__(self):
        db_file = self.__get_database_filename()
        try:
            self.__db_connection = sqlite3.connect(db_file)
            self.__cursor = self.__db_connection.cursor()
        except Error as e:
            print(e)

    def __get_database_filename(self):
        with open('config.json') as json_file:
            data = json.load(json_file)
            return data['sqlite3']['file']

    def close_connection(self):
        self.__cursor.close()
        self.__db_connection.close()

    def create_tables(self):
        self.__cursor.execute('''
                        CREATE TABLE IF NOT EXISTS notification_confirmation (date_ DATE PRIMARY KEY DEFAULT (datetime('now','localtime'))  NOT NULL , notification_sent INTEGER DEFAULT 0);
                  ''')

        self.__cursor.execute('''
                     CREATE TABLE IF NOT EXISTS sensor_data (id INTEGER PRIMARY KEY AUTOINCREMENT, date_ DEFAULT CURRENT_DATE, temperature REAL, humidity REAL, time_recorded  DEFAULT (datetime('now','localtime')) NOT NULL, FOREIGN KEY(date_) REFERENCES notification_confirmation);
                 ''')

    def insert_sensor_data(self, temperature: float, humidity: float):
        self.__cursor.execute('''
                            INSERT INTO sensor_data (temperature, humidity) VALUES (?,?);
                        ''', (temperature, humidity))
        self.__db_connection.commit()

    def insert_notification_confirmation(self):
        self.__cursor.execute('''
                    INSERT INTO notification_confirmation (notification_sent) VALUES (0);
                ''')
        self.__db_connection.commit()

    def check_notification_sent(self):
        self.__cursor.execute('''SELECT notification_sent FROM notification_confirmation WHERE date_ = ?;''',
                              (date.today().__str__(),))

        row = self.__cursor.fetchone()
        return row[0]

    def mark_notification_sent(self):
        self.__cursor.execute('''UPDATE notification_confirmation SET notification_sent = 1 WHERE date_ = ?;''',
                              (date.today().__str__(),))
        self.__db_connection.commit()

    # query the database of all values
    def get_all_sensor_data(self):
        self.__cursor.execute("SELECT id, date_, temperature, humidity FROM sensor_data; ")
        rows = self.__cursor.fetchall()
        return rows

    def get_today_min_temp(self):
        self.__cursor.execute("SELECT temperature FROM sensor_data WHERE date_ = ? order by temperature limit 1",
                              (date.today().__str__(),))
        rows = self.__cursor.fetchall()
        return rows

    def get_today_max_temp(self):
        self.__cursor.execute("SELECT temperature FROM sensor_data WHERE date_ = ? order by temperature desc limit 1",
                              (date.today().__str__(),))
        rows = self.__cursor.fetchall()
        return rows

    def get_today_min_humidity(self):
        self.__cursor.execute("SELECT humidity FROM sensor_data WHERE date_ = ? order by humidity limit 1",
                              (date.today().__str__(),))
        rows = self.__cursor.fetchall()
        return rows

    def get_today_max_humidity(self):
        self.__cursor.execute("SELECT humidity FROM sensor_data WHERE date_ = ? order by humidity desc limit 1",
                              (date.today().__str__(),))
        rows = self.__cursor.fetchall()
        return rows
