from database import greenhouse_monitor_database
from notification import pushbullet
from sense_hat_monitoring import sensor_data
import time
from sqlite3 import Error


class Driver(object):
    @staticmethod
    def monitor_and_notify(db):
        temperature_humidity = sensor_data.SensorData()

        temperature = temperature_humidity.get_temperature()
        humidity = temperature_humidity.get_humidity()

        # log temp and humidity to db
        db.insert_sensor_data(temperature, humidity)

        temp_in_range = temperature_humidity.check_temperature_in_range()
        humid_in_range = temperature_humidity.check_humidity_in_range()

        # if values out of range, if notification not already sent send it and mark it as sent in db
        if (not temp_in_range) or (not humid_in_range):
            title = "Warning! Values out of range."
            body = 'Value out of range: \n\ttemperature: %f\n\thumidity: %f' % (temperature, humidity)
            Driver.send_notification(db, title, body)

    @staticmethod
    def send_notification(db, title, body):
        notification_sent = db.check_notification_sent()

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
