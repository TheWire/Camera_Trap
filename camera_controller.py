import uuid
from camera import Camera
from threading import Lock

class CameraUser():
    def __init__(self, name: str, camera_controller: bool = False):
        self._id = uuid.uuid4()
        self._name = name
        self._camera_controller = camera_controller

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> uuid.UUID:
        return self._id

class CameraController():
    def __init__(self, camera: Camera):
        self.camera = camera
        self._user = CameraUser(name = "camera controller", camera_controller=True)
        self._users = {self._user}
        self._init_locks()
        

    def _init_locks(self):
        self._camera_lock = Lock()
        self._camera_lock_user = None
        self._configuration_lock = None
        self._init_control_locks()

    def _init_control_locks(self):
        self._control_locks = {key: None for key in self.camera.get_controls}


    def _lock_controls_of_type(self, user: CameraUser, control_type_dict: dict[str, tuple])-> tuple[str, str]:
        for control in control_type_dict:
            if self._control_locks[control].keys is not None:
                return (control, self._control_locks[control].name)
        for control in self.camera.get_exposure_controls().keys:
            self._control_locks[control] = user
        return None

    def _unlock_controls_of_type(self, user: CameraUser, control_type_dict: dict[str, tuple]):
        for control in control_type_dict:
            if self._control_locks[control] is None:
                continue
            if self._control_locks[control].id == user.id:
                self._control_locks[control] = None

    def lock_exposure_controls(self, user: CameraUser)-> tuple[str, str]:
        return self._lock_controls_of_type(user, self.camera.get_exposure_controls())

    def unlock_exposure_controls(self, user: CameraUser):
        self._unlock_controls_of_type(user, self.camera.get_exposure_controls())

    def lock_focus_controls(self, user: CameraUser)-> tuple[str, str]:
        return self._lock_controls_of_type(user, self.camera.get_focus_controls())
    
    def unlock_focus_controls(self, user: CameraUser):
        self._unlock_controls_of_type(user, self.camera.get_focus_controls())

    def lock_white_balance_controls(self, user: CameraUser)-> tuple[str, str]:
        return self._lock_controls_of_type(user, self.camera.get_white_balance_controls())
        
    def unlock_white_balance_controls(self, user: CameraUser):
        self._unlock_controls_of_type(user, self.camera.get_white_balance_controls())

    def lock_image_processing_controls(self, user: CameraUser)-> tuple[str, str]:
        return self._lock_controls_of_type(user, self.camera.get_image_processing_controls())
        
    def unlock_image_processing_controls(self, user: CameraUser):
        self._unlock_controls_of_type(user, self.camera.get_image_processing_controls())

    def lock_framerate_controls(self, user: CameraUser)-> tuple[str, str]:
        return self._lock_controls_of_type(user, self.camera.get_framerate_controls())
            
    def unlock_framerate_controls(self, user: CameraUser):
        self._unlock_controls_of_type(user, self.camera.get_framerate_controls())


    def lock_all_controls(self, user: CameraUser)-> tuple[str, str]:
        for control, lock in self._control_locks.item():
            if lock is not None:
                return (control, lock.name)
        for control in self._control_locks.keys():
            self._control_locks[control] = user
        return None

    def unlock_all_controls(self, user: CameraUser):
        for control, lock in self._control_locks.item():
            if lock.id == user.id:
                self._control_locks[control] = None

    def is_control_locked(self, control: str) -> str:
        if self._control_lock[control] is not None:
            return self._control_lock[control].name
        return None
        
    def lock_control(self, user: CameraUser, control: str) -> str:
        control_locked = self.is_control_locked()
        if control_locked is not None:
            return control_locked
        self._control_lock[control] = user
        return None

    def unlock_control(self, user: CameraUser, control: str):
        lock = self._control_locks[control]
        if lock is not None:
            raise ControlLockException("", control, user)
        self._control_locks[control] = None

    def set_control(self, control: str, value, user: CameraUser):
        if self._control_locks[control] == user.id:
            self.lock_camera()
            self.camera.set_control[control] = value
        raise ControlLockException("unable to set control", control, user)
    
    def register_camera_user(self) -> CameraUser:
        user = CameraUser()
        self._users.add(user)
        return user

    def lock_camera(self, user: CameraUser):
        try: 
            self._camera_lock.acquire()
        except:
            raise CameraLockException("camera in user by another process", user)
        self._camera_lock_user = user

    def unlock_camera(self, user: CameraUser):
        self._camera_lock.release()
        self._camera_lock_user = None

    def lock_configuration(self, user: CameraUser) -> str:
        if self._configuration_lock is None:
            self._configuration_lock = user
            return None
        return self._configuration_lock.name

    def unlock_configuration(self, user: CameraUser) -> str:
        if self._configuration_lock is None:
            return None
        if self._configuration_lock.id == user.id:
            self._configuration_lock = None
            return user.name
        return self._configuration_lock.name
        
    def capture(self, path: str):
        self.camera.capture(path)

    def start_recording(self):
        self.camera.start_recording()

    def stop_recording(self):
        self.camera.stop_recording()

    def start_stream(self):
        self.camera.start_stream()

    def stop_stream(self):
        self.camera.stop_stream()

    def generate_http_frames(self):
        yield self.camera.generate_http_frames()
    
class LockException(Exception):
    def __init__(self, message, user: CameraUser):
        self.message = message
        super().__init__(self.message)
        self._user = user

    def __str__(self):
        return f"{self.message} locked by process: {self._user.name}"

class CameraLockException(LockException):
    pass

class ConfigLockException(LockException):
    def __init__(self, message, config: str, user: CameraUser):
        self.message = message
        super().__init__(self.message)
        self._user = user
        self._config = config

    def __str__(self):
        return f"{self.message} config: {self._config} locked by process: {self._user.name}"

class ControlLockException(LockException):
    def __init__(self, message, control: str, user: CameraUser):
        self.message = message
        super().__init__(self.message)
        self._user = user
        self._control = control

    def __str__(self):
        return f"{self.message} control: {self._control} locked by process: {self._user.name}"