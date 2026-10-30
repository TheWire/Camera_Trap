import io
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
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def capture(self, path: str):
        pass

    @abstractmethod
    def start_recording(self):
        pass

    @abstractmethod
    def stop_recording(self):
        pass

    @abstractmethod
    def start_stream(self):
        pass    

    @abstractmethod
    def stop_stream(self):
        pass

    @abstractmethod
    def generate_http_frames(self):
        pass

    @abstractmethod
    def get_exposure_controls(self) -> dict[str, tuple]:
        pass

    @abstractmethod
    def get_focus_controls(self) -> dict[str, tuple]:
        pass

    @abstractmethod
    def get_white_balance_controls(self) -> dict[str, tuple]:
        pass

    @abstractmethod
    def get_image_processing_controls(self) -> dict[str, tuple]:
        pass

    @abstractmethod
    def get_framerate_controls(self) -> dict[str, tuple]:
        pass

    @abstractmethod
    def get_controls(self) -> dict[str, tuple]:
        pass