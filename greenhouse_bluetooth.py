from notification.pushbullet import PushBullet
import threading
import json
from database.greenhouse_monitor_database import GreenhouseMonitorDatabase
import bluetooth


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
            reasons.append("%s less than the minimum temperature. " % line["Min_temp_diff"])
        if line["Max_temp_diff"] != 0:
            status = "Bad"
            reasons.append("%s more than the maximum temperature. " % line["Max_temp_diff"])
        if line["Min_humidity_diff"] != 0:
            status = "Bad"
            reasons.append("%s less than the minimum humidity. " % line["Min_humidity_diff"])
        if line["Max_humidity_diff"] != 0:
            status = "Bad"
            reasons.append("%s more than the maximum humidity. " % line["Max_humidity_diff"])

        reason = ''.join(reasons)
        if status == "Bad":
            pb = PushBullet("Warning!", reason)
            pb.send_notification()


class GreenHouseBluetooth(threading.Thread):
    def run(self):
        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        trusted_devices = "Galaxy_S10"

        for addr, name in nearby_devices:
            if name == trusted_devices:
                notify = BlueToothNotify()

                notify.check_temp_humidity(self.get_range())

    def get_range(self):
        with open('config.json') as json_file:
            data = json.load(json_file)
            return data['data_range']


t = GreenHouseBluetooth()
t.start()
