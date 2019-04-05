from notification.pushbullet import PushBullet
import threading
import json
from database.greenhouse_monitor_database import GreenhouseMonitorDatabase
import bluetooth
import subprocess as sp
import time


class BlueToothNotify:

    def check_temp_humidity(self, range_):
        line = {
            "Min_temp_diff": 0,
            "Max_temp_diff": 0,
            "Min_humidity_diff": 0,
            "Max_humidity_diff": 0
        }
        db = GreenhouseMonitorDatabase()

        if range_["min_temperature"] > db.get_today_min_temp()[0][0]:
            line["Min_temp_diff"] = range_["min_temperature"] - db.get_today_min_temp()[0][0]

        if range_["max_temperature"] < db.get_today_max_temp()[0][0]:
            line["Max_temp_diff"] = db.get_today_max_temp()[0][0] - range_["max_temperature"]

        if range_["min_humidity"] > db.get_today_min_humidity()[0][0]:
            line["Min_humidity_diff"] = range_["min_humidity"] - db.get_today_min_humidity()[0][0]

        if range_["max_humidity"] < db.get_today_max_humidity()[0][0]:
            line["Max_humidity_diff"] = db.get_today_max_humidity()[0][0] - range_["max_humidity"]
        self.notify(line)

    def notify(self, line):
        status = "OK"
        reasons = []
        if line["Min_temp_diff"] != 0:
            status = "Bad"
            reasons.append('\n%s less than the minimum temperature. ' % line["Min_temp_diff"])
        if line["Max_temp_diff"] != 0:
            status = "Bad"
            reasons.append("\n%s more than the maximum temperature. " % line["Max_temp_diff"])
        if line["Min_humidity_diff"] != 0:
            status = "Bad"
            reasons.append("\n%s less than the minimum humidity. " % line["Min_humidity_diff"])
        if line["Max_humidity_diff"] != 0:
            status = "Bad"
            reasons.append("\n%s more than the maximum humidity. " % line["Max_humidity_diff"])

        reason = ''.join(reasons)
        if status == "Bad":
            pb = PushBullet("Warning! Values out of range.", reason)
            pb.send_notification()


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
                    notify = BlueToothNotify()
                    notify.check_temp_humidity(self.get_range())

    def get_range(self):
        with open('config.json') as json_file:
            data = json.load(json_file)
            return data['data_range']


if __name__ == '__main__':
    while True:
        bluetooth_notifications = GreenHouseBluetooth()
        bluetooth_notifications.start()
        time.sleep(3600)
