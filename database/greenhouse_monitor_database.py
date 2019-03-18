import sqlite3
import json
from sqlite3 import Error


class GreenhouseMonitorDatabase(object):
    __db_connection: sqlite3.Connection
    __cursor: sqlite3.Cursor

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
        self.__db_connection.close()
        self.__cursor.close()

    def create_tables(self):
        self.__cursor.execute('''
                        CREATE TABLE IF NOT EXISTS notification_confirmation (id INTEGER PRIMARY KEY AUTOINCREMENT, date DATE DEFAULT CURRENT_DATE NOT NULL , notification_sent INTEGER DEFAULT 0);
                  ''')

        self.__cursor.execute('''
                     CREATE TABLE IF NOT EXISTS sensor_data (id INTEGER PRIMARY KEY AUTOINCREMENT, notification_confirmation_id INTEGER, temperature REAL, humidity REAL, time_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, FOREIGN KEY(notification_confirmation_id) REFERENCES notification_confirmation);
                 ''')

    def insert_sensor_data(self, temperature: float, humidity: float):
        pass
        # self.__cursor.execute('''
        #             INSERT INTO sensor_data VALUE ();
        #         ''')

    def insert_notification_confirmation(self):
        self.__cursor.execute('''
                    INSERT INTO notification_confirmation (notification_sent) VALUES (0);
                ''')
        self.__db_connection.commit()
