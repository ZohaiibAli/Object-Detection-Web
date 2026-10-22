"""Load the YOLO model, run detection and draw the boxes."""
import time

import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO

from backend.config import BOX_COLORS, MAX_IMAGE_SIDE

COLUMNS = ["class_name", "confidence", "x1", "y1", "x2", "y2", "width", "height"]


def load_model(name: str = "yolov8n.pt") -> YOLO:
    """Load a YOLOv8 model (downloaded automatically the first time)."""
    return YOLO(name)


def resize_if_large(image_bgr: np.ndarray, max_side: int = MAX_IMAGE_SIDE) -> np.ndarray:
    """Shrink the image so its longest side is at most max_side pixels."""
    height, width = image_bgr.shape[:2]
    longest = max(height, width)
    if longest <= max_side:
        return image_bgr
    scale = max_side / longest
    new_size = (int(width * scale), int(height * scale))
    return cv2.resize(image_bgr, new_size, interpolation=cv2.INTER_AREA)


def color_for_class(class_id: int) -> tuple:
    """Same class id -> same color, every time."""
    return BOX_COLORS[class_id % len(BOX_COLORS)]


def draw_box(image_rgb: np.ndarray, box, label: str, color: tuple) -> None:
    """Draw one rectangle with a filled label background (edits the image in place)."""
    x1, y1, x2, y2 = [int(v) for v in box]
    cv2.rectangle(image_rgb, (x1, y1), (x2, y2), color, 2)

    font = cv2.FONT_HERSHEY_SIMPLEX
    (text_w, text_h), baseline = cv2.getTextSize(label, font, 0.5, 1)
    # put the label above the box, or inside it if there is no room at the top
    top = max(y1 - text_h - baseline - 4, 0)
    cv2.rectangle(image_rgb, (x1, top), (x1 + text_w + 6, top + text_h + baseline + 4), color, -1)
    cv2.putText(image_rgb, label, (x1 + 3, top + text_h + 2), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)


def detect_objects(model, image_bgr, conf=0.4, iou=0.45, classes=None):
    """Run detection on one BGR image.

    Returns (annotated_image_rgb, detections_df, inference_ms).
    `classes` is an optional list of class names to keep (None = all).
    """
    image_bgr = resize_if_large(image_bgr)
    annotated = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    # translate class names to the ids the model understands
    class_ids = None
    if classes:
        names = model.names  # {id: name}
        class_ids = [i for i, n in names.items() if n in classes]

    start = time.perf_counter()
    results = model.predict(image_bgr, conf=conf, iou=iou, classes=class_ids, device="cpu", verbose=False)
    inference_ms = (time.perf_counter() - start) * 1000

    rows = []
    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        class_id = int(box.cls[0])
        score = float(box.conf[0])
        name = model.names[class_id]
        draw_box(annotated, (x1, y1, x2, y2), f"{name} {score:.2f}", color_for_class(class_id))
        rows.append([name, round(score, 3), int(x1), int(y1), int(x2), int(y2), int(x2 - x1), int(y2 - y1)])

    return annotated, pd.DataFrame(rows, columns=COLUMNS), inference_ms
