from abc import ABC, abstractmethod


class Sensor(ABC):
    """@brief Abstract base class for sensor interfaces.

       Defines the mandatory interface that all sensor classes must implement.
       This ensures consistent behavior across different sensor types.
    """
    @abstractmethod
    def start(self):
        """@brief Start the sensor operation.

           This method must be implemented to initialize and begin sensor
           data acquisition.
        """
        pass

    @abstractmethod
    def stop(self):
        """@brief Stop the sensor operation.

           This method must be implemented to properly shutdown and release
           sensor resources.
        """
        pass

    @abstractmethod
    def get_data(self):
        """@brief Get data from the sensor.

           @return Sensor data in a format specific to the implementation.
           Must be implemented by all concrete sensor classes.
        """
        pass
