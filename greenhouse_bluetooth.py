from notification.pushbullet import PushBullet
import threading
import json
from database.greenhouse_monitor_database import GreenhouseMonitorDatabase
import bluetooth
import subprocess as sp
import logging
from monitorAndNotify import MonitorAndNotify
from sense_hat_monitoring import sensor_data
logging.basicConfig(filename="./logs/bluetooth.log", filemode='a',level=logging.DEBUG)


class GreenHouseBluetooth(threading.Thread):
    def run(self):
        p = sp.Popen(["bt-device", "--list"], stdin=sp.PIPE, stdout=sp.PIPE, close_fds=True)
        (stdout, stdin) = (p.stdout, p.stdin)
        db = GreenhouseMonitorDatabase()
        data = stdout.readlines()
        for devices in data:
            devices = devices.decode("utf-8")
            device = devices[devices.find('(') + 1:devices.find(')')]
            print(device)
            nearby_devices = bluetooth.discover_devices(lookup_names=True)
            trusted_devices = device
            for addr, name in nearby_devices:
                if addr == trusted_devices:
                    temperature_humidity = sensor_data.SensorData()
                    temperature = temperature_humidity.get_temperature()
                    humidity = temperature_humidity.get_humidity()
                    detail='\n Temperature: %.2f *c' %temperature
                    detail+= '\n Humidity:%.2f *c ' %humidity
                    pb = PushBullet("Current values", detail)
                    pb.send_notification()
                    MonitorAndNotify.monitor_and_notify(db)

    def get_range(self):
        with open('config.json') as json_file:
            data = json.load(json_file)
            return data['data_range']


if __name__ == '__main__':
    bluetooth_notifications = GreenHouseBluetooth()
    bluetooth_notifications.start()

