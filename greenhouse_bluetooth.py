from notification.pushbullet import PushBullet
import threading
import json
import time
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
                    delta_temp = temperature_humidity.get_temperature_difference()
                    delta_humidity = temperature_humidity.get_humidity_difference()
                    reasons=MonitorAndNotify.get_notification_detail(delta_temp, delta_humidity)
                    #reasons=GreenHouseBluetooth.get_notification_detail(delta_temp, delta_humidity)
                    if reasons == '':
                        try:
                            pb = PushBullet("Current values", detail)
                            pb.send_notification()
                        except Exception as e:  # any other exceptions
                            logging.warning(e.__str__() + " " + datetime.now().__str__())
                    else:
                        try:
                            pb = PushBullet("Current values", detail+reasons)
                            pb.send_notification()
                        except Exception as e:  # any other exceptions
                            logging.warning(e.__str__() + " " + datetime.now().__str__())

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

    def get_range(self):
        with open('config.json') as json_file:
            data = json.load(json_file)
            return data['data_range']


if __name__ == '__main__':
    bluetooth_notifications = GreenHouseBluetooth()
    bluetooth_notifications.start()

