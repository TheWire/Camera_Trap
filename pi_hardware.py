import numbers
import time
from hardware import Hardware, Device, HardwareException
from gpiozero import MotionSensor, PWMLED, OutputDevice, InputDevice

class PiHardware(Hardware):

    def __init__(self, args: dict[Device, int]):
        self._led = PWMLED(args[Device.light])
        self._motion_sensor = MotionSensor(args[Device.motion])
        self._ldr = args[Device.light_sensor]
        self._light_level = 0

    def light_on(self, level: int):
        if level is None \
            or not isinstance(level, numbers.Number) \
            or level < 0 \
            or level > 100:
                raise HardwareException(device = Device.light, message="invalid light value")
        level_percent = level / 100
        self._light_level =  level_percent
        self._led.value =  level_percent

    @property
    def light_level(self) -> int:
        return self._light_level
    
    def light_off(self):
        self._light_level = 0
        self._led.value = 0

    @property
    def motion_detected(self) -> bool:
        return self._motion_sensor.motion_detected

    def ldr_value(self, charge_time_limit=0.005) -> int:
    
        # Take the pin LOW to discharge the capacitor
        self._ldr = OutputDevice(pin=self._ldr, active_high=True, 
                        initial_value=False)
        time.sleep(0.1)

        # Configure the pin as an input
        ldr.close()
        ldr = InputDevice(pin=self._ldr, pull_up=None,
                        active_state=True)

        # Wait for the capacitor to recharge, but only up to
        # the charge time limit
        lit = 0
        start = time.time()
        while True:
            if time.time() - start >  charge_time_limit:
                break
            if ldr.is_active:
                lit += 1

        ldr.close()
        return lit
