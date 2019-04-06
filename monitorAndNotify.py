#!/usr/bin/env python3
from database import greenhouse_monitor_database
from notification import pushbullet
from sense_hat_monitoring import sensor_data
import time
from datetime import datetime
from sqlite3 import Error
import logging

logging.basicConfig(filename="./logs/greenhouse.log", filemode='a', level=logging.DEBUG)


class MonitorAndNotify(object):
    @staticmethod
    def monitor_and_notify(db):
        temperature_humidity = sensor_data.SensorData()

        temperature = temperature_humidity.get_temperature()
        humidity = temperature_humidity.get_humidity()

        # log temp and humidity to db
        db.insert_sensor_data(temperature, humidity)

        delta_temp = temperature_humidity.get_temperature_difference()
        delta_humidity = temperature_humidity.get_humidity_difference()

        # if values out of range, if notification not already sent send it and mark it as sent in db
        if (delta_temp != 0) or (delta_humidity != 0):
            title = "Warning! Values out of range."
            body = 'Value out of range: \n\ttemperature: %.2f *c\n\thumidity: %.2f %%rH\n\n' % (temperature, humidity)
            body += MonitorAndNotify.get_notification_detail(delta_temp, delta_humidity)
            MonitorAndNotify.send_notification(db, title, body)

    @staticmethod
    def get_notification_detail(delta_temperature, delta_humidity):
        detail = ''

        if delta_temperature > 0:
            detail = '\nTemperature above maximum temperature by %.2f *c' % (delta_temperature,)
        elif delta_temperature < 0:
            detail = '\nTemperature below minimum temperature by %.2f *c' % (-delta_temperature,)

        if delta_humidity > 0:
            detail += '\nHumidity above maximum Humidity by %.2f %%rH' % (delta_humidity,)
        elif delta_humidity < 0:
            detail += '\nHumidity below minimum Humidity by %.2f %%rH' % (-delta_humidity,)

        return detail

    @staticmethod
    def send_notification(db, title, body):

        # if the date changes when program is in execution, insert new row in db for the new date
        try:
            notification_sent = db.check_notification_sent()
        except Error:
            db.insert_notification_confirmation()
            notification_sent = False

        # send notification only if not sent earlier on same date
        if notification_sent == 0:
            notification_sender = pushbullet.PushBullet(title, body)
            notification_sender.send_notification()
            # mark notification sent status in db
            db.mark_notification_sent()

    @staticmethod
    def main():
        db = greenhouse_monitor_database.GreenhouseMonitorDatabase()
        db.create_tables()
        try:
            db.insert_notification_confirmation()
        except:
            pass  # ignore error here

        try:

            while True:
                MonitorAndNotify.monitor_and_notify(db)
                time.sleep(60)
        except Error as e:  # database exceptions
            logging.warning(e.__str__() + " " + datetime.now().__str__())
        except Exception as e:  # any other exceptions
            logging.warning(e.__str__() + " " + datetime.now().__str__())
        finally:
            db.close_connection()


if __name__ == '__main__':
    MonitorAndNotify.main()
