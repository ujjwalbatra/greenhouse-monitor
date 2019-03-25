from database import greenhouse_monitor_database
from notification import pushbullet
from sense_hat_monitoring import sensor_data
import time
from sqlite3 import Error
import math


class Driver(object):
    @staticmethod
    def monitor_and_notify(db):
        temperature_humidity = sensor_data.SensorData()

        temperature = temperature_humidity.get_temperature()
        humidity = temperature_humidity.get_humidity()

        # log temp and humidity to db
        db.insert_sensor_data(temperature, humidity)

        delta_temperature = temperature_humidity.get_delta_temperature()
        delta_humidity = temperature_humidity.get_delta_humidity()

        temp_message, humidity_message = Driver.get_warning_message(delta_temperature, delta_humidity)

        # if values out of range, if notification not already sent send it and mark it as sent in db
        if delta_temperature != 0 or delta_humidity != 0:
            title = 'Warning! Values out of range.'
            body = 'temperature: %.2f' % temperature
            body += '\nhumidity: %.2f' % humidity
            body += '\n\n More Information: %s %s' % (temp_message, humidity_message)
            Driver.send_notification(db, title, body)

    # generates detailed temperature/humidity out of range message
    @staticmethod
    def get_warning_message(delta_temperature, delta_humidity):
        print(delta_temperature)
        print(delta_humidity)
        
        temp_message = ''
        humidity_message = ''
        if delta_temperature > 0:
            temp_message = 'Temperature exceeding max Temperature by %.2f' % delta_temperature
        elif delta_temperature < 0:
            temp_message = 'Temperature below min Temperature by %.2f' % math.fabs(delta_temperature)

        if delta_temperature > 0:
            humidity_message = 'Humidity exceeding max Humidity by %.2f' % delta_temperature
        elif delta_temperature < 0:
            humidity_message = 'Humidity below minimum Humidity by %.2f' % math.fabs(delta_humidity)

        return temp_message, humidity_message

    @staticmethod
    def send_notification(db, title, body):
        notification_sent = db.check_notification_sent()

        #  send notification only if not sent earlier on same date
        if notification_sent == 0:
            notification_sender = pushbullet.PushBullet(title, body)
            notification_sender.send_notification()
            #  mark notification sent status in db
            db.mark_notification_sent()

    @staticmethod
    def main():
        db = greenhouse_monitor_database.GreenhouseMonitorDatabase()
        db.create_tables()
        try:
            db.insert_notification_confirmation()
        except Error:  # ignore error here, error here means that the row is already inserted
            pass

        minutes = 120

        # every minute for 2 hours
        for i in range(minutes):
            Driver.monitor_and_notify(db)
            time.sleep(60)

        db.close_connection()


if __name__ == '__main__':
    Driver.main()
