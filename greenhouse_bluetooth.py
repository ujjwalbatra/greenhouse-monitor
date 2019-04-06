from notification.pushbullet import PushBullet
import threading
import json
import bluetooth
import subprocess as sp
import logging
from monitorAndNotify import MonitorAndNotify
from sense_hat_monitoring import sensor_data
from datetime import datetime

logging.basicConfig(filename="./logs/bluetooth.log", filemode='a', level=logging.DEBUG)


class GreenHouseBluetooth(threading.Thread):
    def run(self):
        p = sp.Popen(["bt-device", "--list"], stdin=sp.PIPE, stdout=sp.PIPE, close_fds=True)
        (stdout, stdin) = (p.stdout, p.stdin)
        data = stdout.readlines()

        for devices in data:
            devices = devices.decode("utf-8")
            device = devices[devices.find('(') + 1:devices.find(')')]

            nearby_devices = bluetooth.discover_devices(lookup_names=True)
            trusted_devices = device

            for addr, name in nearby_devices:
                if addr == trusted_devices:
                    temperature_humidity = sensor_data.SensorData()
                    temperature = temperature_humidity.get_temperature()
                    humidity = temperature_humidity.get_humidity()
                    detail = '\tTemperature: %.2f *c' % temperature
                    detail += '\n\tHumidity: %.2f *c' % humidity

                    # get temperature and humidity difference
                    delta_temp = temperature_humidity.get_temperature_difference()
                    delta_humidity = temperature_humidity.get_humidity_difference()

                    reasons = MonitorAndNotify.get_notification_detail(delta_temp, delta_humidity)
                    # if values out of range add warning message

                    if reasons == '':
                        pb = PushBullet("Current values", detail)
                        pb.send_notification()

                    else:
                        pb = PushBullet("Current values", detail + reasons)
                        pb.send_notification()

    def get_range(self):
        with open('config.json') as json_file:
            data = json.load(json_file)
            return data['data_range']


if __name__ == '__main__':
    try:
        bluetooth_notifications = GreenHouseBluetooth()
        bluetooth_notifications.start()
    except Exception as e:  # any other exceptions
        logging.warning(e.__str__() + " " + datetime.now().__str__())
