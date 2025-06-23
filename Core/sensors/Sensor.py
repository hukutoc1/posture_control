from abc import ABC, abstractmethod


class Sensor(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def get_data(self):
        pass
