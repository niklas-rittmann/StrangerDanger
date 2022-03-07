import os
from pathlib import Path

import cv2
import numpy as np
from watchdog.events import FileSystemEventHandler
from watchdog.observers.polling import PollingObserver

from stranger_danger.constants.image_constants import H, W
from stranger_danger.detector.detector import Detector

DIRECTORY_TO_WATCH = os.getenv("DIRECTORY_TO_WATCH")


def load_resize_image(path: Path) -> np.ndarray:
    """Resize image to desired size"""
    image = cv2.imread(path)
    return cv2.resize(image, (H, W), interpolation=cv2.INTER_AREA)


class FilesytemWatcher:
    def __init__(self, detector: Detector, status: bool) -> None:
        # Use PollingObserver to be able to watch network drives as well
        self.filewatcher = PollingObserver()
        self.detector = detector
        self.status: bool = status

    def run_watcher(self) -> None:
        """Start the filesystem watcher"""
        self.filewatcher.schedule(
            FileHandler(self.detector), DIRECTORY_TO_WATCH, recursive=True
        )
        self.filewatcher.start()

    def stop_watcher(self) -> None:
        """Check if the filewatcher should remain running"""
        self.filewatcher.stop()
        self.filewatcher.join()

    @property
    def is_running(self) -> bool:
        return self.filewatcher.is_alive()


class FileHandler(FileSystemEventHandler):
    def __init__(self, detector: Detector) -> None:
        super().__init__()
        self.detector = detector

    def on_created(self, event):
        """Check which event occured"""
        if not event.is_directory and event.src_path.endswith("jpg"):
            image = load_resize_image(event.src_path)
            self.detector.run_detector(image)
