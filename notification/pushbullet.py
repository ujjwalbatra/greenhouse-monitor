import requests
import json


class PushBullet(object):
    __headers = {
        'Content-Type': 'application/json',
    }
    __notification_type = 'note'
    __access_token = ''

    def __init__(self, title, body):
        self.__data = json.dumps({"type": self.__notification_type, "title": title, "body": body})
        self.__initialise_pushbullet_access_token()

    def send_notification(self):
        requests.post('https://api.pushbullet.com/v2/pushes', headers=self.__headers, data=self.__data,
                      auth=(self.__access_token, ''))

    def __initialise_pushbullet_access_token(self):
        with open('config.json') as json_file:
            data = json.load(json_file)
            self.__access_token = data['pushbullet']['access_token']
