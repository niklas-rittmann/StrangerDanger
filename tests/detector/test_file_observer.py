import time

from stranger_danger.detector import event_listener as ev_l
from stranger_danger.detector.detector import Detector


def test_start_stop(detector: Detector, monkeypatch):
    """Test if its possible to start and stop the watcher"""
    monkeypatch.setattr(ev_l, "DIRECTORY_TO_WATCH", ".")
    watcher = ev_l.FilesytemWatcher(detector, True)
    watcher.run_watcher()
    assert watcher.is_running
    watcher.stop_watcher()
    assert not watcher.is_running
