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
    __temperature = None
    __humidity = None

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

    #  returns difference in temperature from range in config.returns +ve value if more than max, -ve is less than min
    def get_delta_temperature(self):
        with open('config.json') as json_file:
            data = json.load(json_file)
            min_temp = data['data_range']['min_temperature']
            max_temp = data['data_range']['max_temperature']

        if max_temp < self.__temperature:
            delta_temperature = self.__temperature - max_temp
            return delta_temperature
        elif min_temp > self.__temperature:
            delta_temperature = min_temp - self.__temperature
            return delta_temperature
        else:
            return 0

    #  returns difference in humidity from range in config.returns +ve value if more than max, -ve is less than min
    def get_delta_humidity(self):
        with open('config.json') as json_file:
            data = json.load(json_file)
            min_humidity = data['data_range']['min_humidity']
            max_humidity = data['data_range']['max_humidity']

        if max_humidity < self.__temperature:
            delta_temperature = self.__temperature - max_humidity
            return delta_temperature
        elif min_humidity > self.__temperature:
            delta_temperature = min_humidity - self.__temperature
            return delta_temperature
        else:
            return 0
