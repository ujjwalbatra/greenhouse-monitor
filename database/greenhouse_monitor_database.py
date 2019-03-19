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
            print(sqlite3.version)
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
            CREATE TABLE IF NOT EXISTS notification_confirmation (date DATE DEFAULT CURRENT_DATE NOT NULL , notification_sent INTEGER);
        ''')

        self.__cursor.execute('''
                    CREATE TABLE IF NOT EXISTS sensor_data (id INTEGER PRIMARY KEY AUTOINCREMENT, temperature REAL, humidity REAL, time_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL);
        ''')

    def insert_to_db(self, temperature: float, humidity: float):
        print("Works")
        print(temperature)
        self.__cursor.execute("INSERT INTO sensor_data (temperature, humidity) VALUES (?,?);",(temperature,humidity))

    def query_to_db(self):
        self.__cursor.execute("SELECT * FROM sensor_data; ")
 
        rows = self.__cursor.fetchall()
        print("Works")
        for row in rows:
            print(row)