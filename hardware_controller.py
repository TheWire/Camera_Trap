from hardware import Hardware

class HardwareController:
    def __init__(self, hardware: Hardware):
        self._hardware = hardware

    def light_on(self, level: int):
        self._hardware.light_on(level)

    def light_off(self):
        self._hardware.light_off()

    @property
    def light_level(self) -> int:
        return self._hardware.light_level

    def ldr_value(self, charge_time_limit=0.005) -> int:
        return self._hardware.ldr_value

    @property
    def motion_detected(self) -> bool:
        return self._hardware.motion_detected