"""About page."""
import pandas as pd
import streamlit as st

from backend.config import COCO_CLASSES
from utils.ui import setup_page

setup_page("About <em>VisionScan</em>", "A computer-vision course project.", eyebrow="About")

st.header("Overview")
st.write("VisionScan detects objects in images, videos and webcam photos using a pretrained "
         "YOLOv8 model, draws bounding boxes with labels and confidence scores, and keeps "
         "analytics of every run.")

st.header("Technology stack")
st.markdown("""
- **Streamlit** - web interface
- **Ultralytics YOLOv8** (PyTorch, CPU) - object detection
- **OpenCV** - image reading, resizing and drawing boxes
- **imageio + ffmpeg** - writing browser-playable H.264 video
- **SQLite + pandas** - history storage
- **Plotly** - charts
- **FastAPI** (optional) - REST endpoint `POST /detect`
""")

st.header("How YOLO works (in simple words)")
st.markdown("""
- **Single pass:** YOLO = "You Only Look Once". The whole image goes through the network one time, which makes it fast.
- **Grid / anchor-free head:** the image is divided into a grid. Each grid cell predicts the box of an object centred there. YOLOv8 predicts the box directly and does not need pre-defined anchor boxes.
- **Confidence score:** a number from 0 to 1 saying how sure the model is. Boxes below the threshold are dropped.
- **IoU (Intersection over Union):** how much two boxes overlap (overlap area / combined area).
- **Non-Max Suppression (NMS):** many boxes may cover the same object. NMS keeps the one with the highest confidence and removes others whose IoU with it is above the IoU threshold.
""")

st.header("Model comparison")
st.table(pd.DataFrame({
    "Model": ["yolov8n", "yolov8s"],
    "File size": ["~6 MB", "~22 MB"],
    "Parameters": ["3.2 M", "11.2 M"],
    "CPU speed": ["Faster", "Slower (~2-3x)"],
    "COCO mAP50-95": [37.3, 44.9],
}))

with st.expander("The 80 COCO classes"):
    st.write(", ".join(COCO_CLASSES))

st.header("Limitations")
st.markdown("""
- Only the 80 COCO classes can be detected.
- Small, blurry or heavily hidden objects are often missed.
- Runs on CPU, so large videos are slow (only the first 30 s are processed).
- Webcam mode takes one photo at a time, not a live stream.
""")

st.header("Future improvements")
st.markdown("""
- Live webcam streaming with WebRTC
- Train on a custom dataset
- Object tracking across video frames
- Instance segmentation and pose estimation
""")

st.header("Team / Author")
st.write("**Name:** Your Name Here  \n**Roll No:** 000000  \n**Course:** Computer Vision  \n**Instructor:** Instructor Name")
