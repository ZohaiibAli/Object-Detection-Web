# 🎯 VisionScan – Real-Time Object Detection Web App

Upload an image, a video, or use your webcam. VisionScan detects objects with a pretrained **YOLOv8** model, draws bounding boxes with labels and confidence scores, and shows analytics of every run.

## Live Demo
👉 https://YOUR-APP-NAME.streamlit.app

## Screenshots
| Home | Image detection | Analytics |
|---|---|---|
| _(add screenshot)_ | _(add screenshot)_ | _(add screenshot)_ |

## Features
- **Image detection** – upload or pick a sample, side-by-side original/annotated view, metrics, table, chart, PNG/CSV download
- **Video detection** – first 30 s / 600 frames, progress bar, browser-playable H.264 output, per-frame and per-class charts
- **Webcam detection** – take a photo in the browser (`st.camera_input`), no WebRTC needed
- **Analytics & history** – SQLite history, charts, filter, CSV export, clear history
- Sidebar settings: model (`yolov8n` / `yolov8s`), confidence, IoU, class filter
- Optional **FastAPI** endpoint `POST /detect`

## Tech stack
Streamlit · Ultralytics YOLOv8 (PyTorch CPU) · OpenCV (headless) · imageio + ffmpeg · SQLite · pandas · Plotly · FastAPI

## Architecture
```
 Streamlit UI (app.py, pages/, utils/ui.py)
        │  calls
        ▼
 backend/  ── detector.py     load model, detect, draw boxes
           ── video_utils.py  frame-by-frame video + H.264 writer
           ── database.py     SQLite history (detections.db)
           ── config.py       constants
        ▲
        │  same code reused by
 api.py (optional FastAPI: GET /health, POST /detect)
```

## Folder structure
```
visionscan/
├── app.py                  Home page
├── pages/                  1_Image, 2_Video, 3_Webcam, 4_Analytics_History, 5_About
├── backend/                detector.py, video_utils.py, database.py, config.py
├── utils/ui.py             shared CSS, header, sidebar, result display
├── api.py                  optional FastAPI
├── scripts/download_samples.py
├── sample_data/            sample images
├── tests/test_detector.py  pytest smoke tests
├── .streamlit/config.toml
├── requirements.txt  packages.txt  runtime.txt  Dockerfile
└── README.md  DEPLOYMENT.md
```

## Local setup
```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate        macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt
python scripts/download_samples.py      # optional sample images
streamlit run app.py
```
The first run downloads `yolov8n.pt` automatically.

## Optional FastAPI
```bash
uvicorn api:app --reload
# then open http://127.0.0.1:8000/docs  or:
curl -X POST -F "file=@sample_data/bus.jpg" -F "conf=0.4" -F "iou=0.45" http://127.0.0.1:8000/detect
```
The Streamlit app does **not** need the API to be running.

## Tests
```bash
pytest
```

## How the detection pipeline works
1. The image is decoded with OpenCV and resized so its longest side is ≤ 1280 px.
2. YOLOv8 runs one forward pass and outputs boxes, classes and confidence scores.
3. Boxes below the confidence threshold are dropped; Non-Max Suppression (IoU threshold) removes duplicates.
4. Each remaining box is drawn with OpenCV in a color fixed per class.
5. Results go to a pandas table, charts, and the SQLite history.

For video, steps 1–4 run on every Nth frame and the frames are written to an H.264 `mp4` with imageio.

## Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md).
