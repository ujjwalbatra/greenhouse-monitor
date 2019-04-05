from sense_hat import SenseHat
from abc import abstractmethod
import json


class ReadTemperature:
    @abstractmethod
    def get_current_temperature(self, sense):
        pass


class ReadHumidity:
    @abstractmethod
    def get_current_humidity(self, sense):
        pass


class SensorData(ReadTemperature, ReadHumidity):
    __temperature = 0.0
    __humidity = 0.0

    def __init__(self):
        sense = SenseHat()
        sense.clear()
        self.__temperature = self.get_current_temperature(sense)
        self.__humidity = self.get_current_humidity(sense)

    def get_current_temperature(self, sense):
        return sense.get_temperature()

    def get_current_humidity(self, sense):
        return sense.get_humidity()

    def get_temperature(self):
        return self.__temperature

    def get_humidity(self):
        return self.__humidity

    def get_temperature_difference(self):
        with open('config.json') as json_file:
            data = json.load(json_file)
            min_temp = data['data_range']['min_temperature']
            max_temp = data['data_range']['max_temperature']

        if max_temp < self.__temperature:
            return self.__temperature - max_temp
        elif min_temp > self.__temperature:
            return self.__temperature - min_temp
        else:
            return 0

    def get_humidity_difference(self):
        with open('config.json') as json_file:
            data = json.load(json_file)
            min_humidity = data['data_range']['min_humidity']
            max_humidity = data['data_range']['max_humidity']

        if max_humidity < self.__humidity:
            return self.__humidity - max_humidity
        elif min_humidity > self.__humidity:
            return self.__humidity - min_humidity
        else:
            return 0
