import os
import queue
from threading import Thread
import multiprocessing as mp
from PIL import Image


class Thumbnailer(Thread):
    def __init__(self, path, thumbnail_path):
        super().__init__()
        self.path = path
        self.thumbnail_path = thumbnail_path
        self.thumb_queue = mp.UniqueQueue()
        self.worker = mp.Process(
            target=self.thumbnail_worker,
            args=(self.thumb_queue,),
            daemon=True
        )
        

    def run(self):
        self.worker.start()
        try:
            while True:    
                try:
                    for image in get_files_to_thumb(self.path, self.thumbnail_path):
                        self.thumb_queue.put_nowait(os.path.join(self.path, image))
                except mp.queues.Full:
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
    ext = str.lower(file.suffix)
    return ext == "jpg" or ext == "jpeg"

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

class UniqueQueue(mp.queues.Queue):
    def __init__(self, *args, **kwargs):
        ctx = mp.get_context()
        super().__init__(*args, ctx=ctx, **kwargs)
        
        self._manager = ctx.Manager()
        self._seen_items = self._manager.set()
        self._lock = ctx.Lock()

    def put(self, obj, block=True, timeout=None):
        """Overrides put() to only add items if they aren't already queued."""
        with self._lock:
            if obj not in self._seen_items:
                self._seen_items.add(obj)
                super().put(obj, block, timeout)
                return True
            return False

    def get(self, block=True, timeout=None):
        """Overrides get() to remove the item from tracking upon extraction."""
        item = super().get(block, timeout)
        with self._lock:
            self._seen_items.discard(item)
        return item
