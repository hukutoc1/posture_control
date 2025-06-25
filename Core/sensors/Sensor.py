from abc import ABC, abstractmethod


class Sensor(ABC):
    """Abstract base class for sensor interfaces.

       Defines the mandatory interface that all sensor classes must implement.
       This ensures consistent behavior across different sensor types.
    """

    @abstractmethod
    def start(self):
        """Start the sensor operation.

           This method must be implemented to initialize and begin sensor
           data acquisition.
        """
        pass

    @abstractmethod
    def stop(self):
        """Stop the sensor operation.

           This method must be implemented to properly shutdown and release
           sensor resources.
        """
        pass

    @abstractmethod
    def get_data(self):
        """Get data from the sensor.

        Returns:
            Any: Sensor data in a format specific to the implementation.

        Raises:
            NotImplementedError: If the method is not overridden in a subclass.
        """
        pass
