from abc import ABC, abstractmethod
from threading import Condition

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self,buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class Camera(ABC):
    def __init__(self):
        pass
