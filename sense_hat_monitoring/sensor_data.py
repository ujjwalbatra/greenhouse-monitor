from sense_hat import SenseHat
from abc import abstractmethod


class ReadTemperature():
    @abstractmethod
    def get_current_temperature(self, sense):
        pass


class ReadHumidity():
    @abstractmethod
    def get_current_humidity(self, sense):
        pass


class SensorData(ReadTemperature, ReadHumidity):
    __temperature: float
    __humidity: float

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
