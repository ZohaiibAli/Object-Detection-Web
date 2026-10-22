"""Smoke tests. Run with: pytest"""
import sys
from pathlib import Path

import cv2
import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend import database  # noqa: E402
from backend.detector import COLUMNS, detect_objects, load_model, resize_if_large  # noqa: E402

SAMPLE_DIR = Path(__file__).resolve().parent.parent / "sample_data"


@pytest.fixture(scope="module")
def model():
    return load_model("yolov8n.pt")


def sample_image():
    """First sample image, or a blank image if none was downloaded."""
    files = sorted(SAMPLE_DIR.glob("*.jpg"))
    if files:
        return cv2.imread(str(files[0]))
    return np.zeros((480, 640, 3), dtype=np.uint8)


def test_detection_output(model):
    image = sample_image()
    annotated, df, ms = detect_objects(model, image, conf=0.4, iou=0.45)
    assert annotated.ndim == 3 and annotated.shape[2] == 3
    assert list(df.columns) == COLUMNS
    assert ms > 0


def test_class_filter(model):
    _, df, _ = detect_objects(model, sample_image(), classes=["person"])
    assert set(df["class_name"]).issubset({"person"})


def test_resize_large_image():
    big = np.zeros((2000, 3000, 3), dtype=np.uint8)
    assert max(resize_if_large(big).shape[:2]) == 1280


def test_database_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")
    database.save_record("image", "a.jpg", "yolov8n.pt", 0.4, 2, 50.0, {"person": 2})
    history = database.get_history()
    assert len(history) == 1 and history.iloc[0]["num_objects"] == 2
    database.clear_history()
    assert database.get_history().empty
