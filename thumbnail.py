import os
import multiprocessing as mp
from queue import Full
import pathlib
from threading import Thread, Event
from PIL import Image


class Thumbnailer(Thread):
    def __init__(self, path, thumbnail_path):
        super().__init__()
        self._stop_event = Event()
        self.path = path
        self.thumbnail_path = thumbnail_path
        self.thumb_queue = UniqueQueue()
        self.worker = mp.Process(
            target=thumbnail_worker,
            args=(path, self.thumb_queue,),
            daemon=True
        )

    def stop(self):
        self._stop_event.set()
        
    def stopped(self):
         return self._stop_event.is_set()
        

    def run(self):
        self.worker.start()
        try:
            while True:    
                try:
                    for image in get_files_to_thumb(self.path, self.thumbnail_path):
                        self.thumb_queue.put(os.path.join(self.path, image))
                except Full:
                    print("thumbnail queue full skipping this one")

        finally:
            self.thumb_queue.put(None)
            self.worker.join(timeout=5)


def thumbnail_worker(path, queue: mp.Queue, thumb_size=(400, 300), quality=85):
    while True:
        path = queue.get()          
        if path is None:     
            break
        try:
            base, ext = os.path.splitext(path)
            thumb_path = f"{base}_thumb{ext}"

            if os.path.exists(thumb_path):
                continue
            with Image.open(path) as img:
                img.thumbnail(thumb_size, Image.Resampling.LANCZOS)
                img.save(thumb_path, "JPEG", quality=quality, optimize=True)
        except Exception as e:
            print(f"[thumb] error on {path}: {e}")

def is_jpeg(file):
    ext = str.lower(pathlib.Path(file).suffix)
    return ext == ".jpg" or ext == ".jpeg"

def get_filename_from_thumb(thumb):
    base, ext = os.path.splitext(thumb)
    return f"{base.removesuffix('_thumb')}{ext}"

def thumb_name(file):
    base, ext = os.path.splitext(file)
    return f"{base}_thumb{ext}"

def get_files_to_thumb(path, thumbpath):
    images = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and (is_jpeg(f))]
    thumbnails = os.listdir(thumbpath)
    return [image for image in images if thumb_name(image) not in thumbnails]

class UniqueQueue:
    def __init__(self, *args, **kwargs):
        self._ctx = mp.get_context()
        self._queue = self._ctx.Queue(*args, **kwargs)

        self._manager = self._ctx.Manager()
        self._seen_items = self._manager.dict()
        self._lock = self._ctx.Lock()

    def put(self, obj, block=True, timeout=None):
        with self._lock:
            if obj not in self._seen_items:
                try:
                    self._queue.put(obj, block=block, timeout=timeout)
                    self._seen_items[obj] = True
                    return True
                except Full:
                    print("thumbnail queue full skipping this one")
                    return False
            return False

    def get(self, block=True, timeout=None):
        item = self._queue.get(block, timeout)
        with self._lock:
            self._seen_items.pop(item, None)
        return item

    def qsize(self):
        return self._queue.qsize()

    def empty(self):
        return self._queue.empty()

    def full(self):
        return self._queue.full()

    def close(self):
        self._queue.close()
