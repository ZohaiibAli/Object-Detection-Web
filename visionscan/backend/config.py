"""Constants used by the whole project."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLE_DIR = BASE_DIR / "sample_data"
DB_PATH = BASE_DIR / "detections.db"

MODEL_OPTIONS = ["yolov8n.pt", "yolov8s.pt"]
DEFAULT_MODEL = "yolov8n.pt"

DEFAULT_CONF = 0.40
DEFAULT_IOU = 0.45

MAX_IMAGE_SIDE = 1280          # resize larger images before inference
ALLOWED_IMAGE_TYPES = ["jpg", "jpeg", "png", "webp"]
ALLOWED_VIDEO_TYPES = ["mp4", "avi", "mov", "mkv"]

MAX_VIDEO_SECONDS = 30         # only process the first 30 seconds ...
MAX_VIDEO_FRAMES = 600         # ... or 600 frames, whichever comes first
DEFAULT_FRAME_SKIP = 2

# The 80 COCO class names, in the order used by YOLOv8
COCO_CLASSES = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
    "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
    "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball",
    "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
    "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
    "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse",
    "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
    "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier",
    "toothbrush",
]

# A fixed palette; each class id always maps to the same color (RGB)
BOX_COLORS = [
    (230, 25, 75), (60, 180, 75), (255, 180, 0), (0, 130, 200), (245, 130, 48),
    (145, 30, 180), (70, 240, 240), (240, 50, 230), (210, 245, 60), (250, 190, 212),
    (0, 128, 128), (220, 190, 255), (170, 110, 40), (128, 0, 0), (128, 128, 0), (0, 0, 128),
]
