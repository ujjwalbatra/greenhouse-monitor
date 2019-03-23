import requests
import json


class PushBullet(object):
    __headers = {
        'Content-Type': 'application/json',
    }
    __notification_type = 'note'
    __data: str

    def __init__(self, title, body):
        self.__data = json.dumps({"type": self.__notification_type, "title": title, "body": body})

    def send_notification(self):
        response = requests.post('https://api.pushbullet.com/v2/pushes', headers=self.__headers, data=self.__data,
                                 auth=('o.irAFuzgjn6N2TshmJm5ZApQxWXddQfX9', ''))


