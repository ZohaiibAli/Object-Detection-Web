"""Optional FastAPI wrapper around the same detector. Run: uvicorn api:app --reload"""
import cv2
import numpy as np
from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from backend.detector import detect_objects, load_model

app = FastAPI(title="VisionScan API")
_model = None


def get_model():
    """Load the model on first use only."""
    global _model
    if _model is None:
        _model = load_model("yolov8n.pt")
    return _model


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/detect")
async def detect(file: UploadFile = File(...), conf: float = Form(0.4), iou: float = Form(0.45)):
    data = await file.read()
    image = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid image.")

    _, df, inference_ms = detect_objects(get_model(), image, conf, iou)
    return {
        "count": len(df),
        "inference_ms": round(inference_ms, 1),
        "detections": df.to_dict(orient="records"),
    }
