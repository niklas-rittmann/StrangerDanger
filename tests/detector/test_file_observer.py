import cv2
import numpy as np

from stranger_danger.constants.image_constants import H, W
from stranger_danger.detector import event_listener as ev_l
from stranger_danger.detector.detector import Detector


def test_resize_image(monkeypatch):
    """Test the resizing of images"""
    monkeypatch.setattr(cv2, "imread", lambda _: np.zeros((1000, 1000, 3)))
    image = ev_l.load_resize_image("bla")
    assert isinstance(image, np.ndarray)
    assert image.shape == (H, W, 3)


def test_start_stop(detector: Detector, monkeypatch):
    """Test if its possible to start and stop the watcher"""
    monkeypatch.setattr(ev_l, "DIRECTORY_TO_WATCH", ".")
    watcher = ev_l.FilesytemWatcher(detector, True)
    watcher.run_watcher()
    assert watcher.is_running
    watcher.stop_watcher()
    assert not watcher.is_running
