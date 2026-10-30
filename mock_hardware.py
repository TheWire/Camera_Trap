from hardware import Hardware
from pprint import pprint
from random import random

class MockHardware(Hardware):

    def __init__(self, args: dict[Device, any]):
        self._light_level = 0
        print("init mock hardware")
        pprint(args)

    def light_on(self, level: int):
        print(f"mock light on at level: {level}")

    def light_off(self):
        print(f"mock light off")

    @property
    def light_level(self) -> int:
        return self._light_level

    def ldr_value(self, charge_time_limit=0.005) -> int:
        r = random.randint(1,20)
        print(f"mock ldr value {r}")
        return r

    @property
    def motion_detected(self) -> bool:
        r = random.randint(1,100)
        if r == 1:
            print("mock motion detected")
            return True
        return False