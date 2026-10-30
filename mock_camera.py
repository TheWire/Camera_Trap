from camera import Camera

class MockCamera(Camera):

    def __init__(self):
        pass

    def capture(self, path: str):
        print(f"mock camera capture stored in {path}")

    def start_recording(self):
        print(f"mock camera start record")

    def stop_recording(self):
        print(f"mock camera stop record")

    def start_stream(self):
        print(f"mock camera start stream")    

    def stop_stream(self):
        print(f"mock camera stop stream")

    def generate_http_frames(self):
        pass

    def get_exposure_controls(self) -> dict[str, tuple]:
        pass

    def get_focus_controls(self) -> dict[str, tuple]:
        pass

    def get_white_balance_controls(self) -> dict[str, tuple]:
        pass

    def get_image_processing_controls(self) -> dict[str, tuple]:
        pass

    def get_framerate_controls(self) -> dict[str, tuple]:
        pass

    def get_controls(self) -> dict[str, tuple]:
        pass
