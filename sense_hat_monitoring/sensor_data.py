class ReadTemperature:
    def get_current_temperature(self):
        pass


class ReadHumidity:
    def get_current_humidity(self):
        pass


class SensorData(ReadTemperature, ReadHumidity):
    def __init__(self, temperature, humidity):
        self.__temperature = temperature
        self.__humidity = humidity

    def get_current_humidity(self):
        pass

    def get_current_temperature(self):
        pass
