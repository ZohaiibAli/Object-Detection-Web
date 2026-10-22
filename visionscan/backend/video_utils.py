"""Frame-by-frame video processing."""
import time
from pathlib import Path

import cv2
import imageio

from backend.config import MAX_VIDEO_FRAMES, MAX_VIDEO_SECONDS
from backend.detector import detect_objects


def process_video(model, input_path, output_path, conf=0.4, iou=0.45, classes=None,
                  frame_skip=2, progress_callback=None):
    """Detect objects in a video and write an H.264 mp4 that browsers can play.

    Detection runs on every `frame_skip`-th frame; the frames in between
    reuse the last annotated frame so the output keeps its full length.
    Returns a summary dictionary.
    """
    cap = cv2.VideoCapture(str(input_path))
    if not cap.isOpened():
        raise ValueError("Could not open the video file. It may be corrupt or unsupported.")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    file_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or MAX_VIDEO_FRAMES
    frame_limit = min(file_frames, MAX_VIDEO_FRAMES, int(fps * MAX_VIDEO_SECONDS))
    frame_skip = max(1, int(frame_skip))

    writer = imageio.get_writer(str(output_path), fps=fps, codec="libx264",
                                pixelformat="yuv420p", macro_block_size=2)
    class_counts = {}
    detections_per_frame = []
    total_detections = 0
    frames_processed = 0
    last_annotated = None
    start = time.perf_counter()

    try:
        for frame_index in range(frame_limit):
            ok, frame = cap.read()
            if not ok:
                break

            if frame_index % frame_skip == 0 or last_annotated is None:
                annotated, df, _ = detect_objects(model, frame, conf, iou, classes)
                last_annotated = _even_size(annotated)
                frames_processed += 1
                total_detections += len(df)
                detections_per_frame.append(len(df))
                for name in df["class_name"]:
                    class_counts[name] = class_counts.get(name, 0) + 1

            writer.append_data(last_annotated)
            if progress_callback:
                progress_callback((frame_index + 1) / frame_limit)
    finally:
        cap.release()
        writer.close()

    elapsed = max(time.perf_counter() - start, 1e-6)
    return {
        "frames_processed": frames_processed,
        "average_fps": round(frames_processed / elapsed, 2),
        "total_detections": total_detections,
        "class_counts": class_counts,
        "detections_per_frame": detections_per_frame,
        "output_path": str(Path(output_path)),
    }


def _even_size(image):
    """H.264 with yuv420p needs even width and height."""
    height, width = image.shape[:2]
    return image[: height - height % 2, : width - width % 2]
