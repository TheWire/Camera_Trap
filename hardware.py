from abc import ABC, abstractmethod
from enum import Enum, StrEnum 

class Device(StrEnum):
    light = "LIGHT"
    motion = "MOTION"
    light_sensor = "LIGHT_SENSOR"

class HardWareExceptionCode(Enum):
    invalid_light_level = 1

class HardwareException(Exception):
    def __init__(self, message, code: HardWareExceptionCode, device: Device):
        self.message = message
        self.code = code
        super().__init__(self.message)
    
    def __str__(self):
        return f"error {self.code} - device: {self.device} - {self.message}" 

class Hardware(ABC):

    @abstractmethod
    def __init__(self, args: dict[Device, any]):
        pass

    @abstractmethod
    def light_on(self, level: int):
        pass

    @abstractmethod
    def light_off(self):
        pass

    @abstractmethod
    def light_level(self) -> int:
        pass

    @abstractmethod
    def ldr_value(self, charge_time_limit=0.005) -> int:
        pass

    @abstractmethod
    def motion_detected(self) -> bool:
        pass

