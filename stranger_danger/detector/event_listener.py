import os
import time

import cv2
from watchdog.events import FileSystemEventHandler
from watchdog.observers.polling import PollingObserver

from stranger_danger.detector.detector import Detector

DIRECTORY_TO_WATCH = os.getenv("DIRECTORY_TO_WATCH")


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
        self.check_watcher()

    def check_watcher(self) -> None:
        """Check if the filewatcher should remain running"""
        while self.status:
            time.sleep(3)
        self.filewatcher.stop()
        self.filewatcher.join()


class FileHandler(FileSystemEventHandler):
    def __init__(self, detector: Detector) -> None:
        super().__init__()
        self.detector = detector

    def on_created(self, event):
        """Check which event occured"""
        if not event.is_directory and event.src_path.endswith("jpg"):
            image = cv2.imread(event.src_path)
            self.detector.run_detector(image)