"""Shared UI pieces: CSS, page header, sidebar settings, result display."""
import io

import cv2
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image

from backend import config
from backend.detector import detect_objects, load_model

CSS = """
<style>
.gradient-title {
    font-size: 2.6rem; font-weight: 800;
    background: linear-gradient(90deg, #6366f1, #ec4899);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.subtitle { font-size: 1.1rem; opacity: 0.75; margin-bottom: 1rem; }
.card {
    border: 1px solid rgba(128,128,128,0.3); border-radius: 14px;
    padding: 1.1rem 1.3rem; height: 100%;
    background: rgba(128,128,128,0.07);
}
.card h3 { margin-top: 0; }
div[data-testid="stMetric"] {
    border: 1px solid rgba(128,128,128,0.3); border-radius: 12px;
    padding: 0.8rem 1rem; background: rgba(128,128,128,0.07);
}
.stButton > button, .stDownloadButton > button { border-radius: 10px; font-weight: 600; }
</style>
"""


def setup_page(title: str, subtitle: str = "") -> None:
    """Page config + CSS + gradient header. Call first on every page."""
    st.set_page_config(page_title="VisionScan", page_icon="🎯", layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(f'<div class="gradient-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="subtitle">{subtitle}</div>', unsafe_allow_html=True)


@st.cache_resource(show_spinner="Loading YOLOv8 model...")
def get_model(name: str):
    """Load the model once and keep it in memory."""
    return load_model(name)


def sidebar_settings() -> dict:
    """Draw the settings in the sidebar. Values are kept in st.session_state across pages."""
    state = st.session_state
    state.setdefault("model_name", config.DEFAULT_MODEL)
    state.setdefault("conf", config.DEFAULT_CONF)
    state.setdefault("iou", config.DEFAULT_IOU)
    state.setdefault("classes", list(config.COCO_CLASSES))

    st.sidebar.header("⚙️ Detection settings")
    model_name = st.sidebar.selectbox("Model", config.MODEL_OPTIONS,
                                      index=config.MODEL_OPTIONS.index(state["model_name"]))
    conf = st.sidebar.slider("Confidence threshold", 0.05, 0.95, float(state["conf"]), 0.05)
    iou = st.sidebar.slider("IoU threshold", 0.10, 0.95, float(state["iou"]), 0.05)
    classes = st.sidebar.multiselect("Classes to detect", config.COCO_CLASSES, default=state["classes"])

    # save back so the values survive when the user switches page
    state.update(model_name=model_name, conf=conf, iou=iou, classes=classes)

    if not classes:
        st.sidebar.warning("No class selected - all classes will be used.")
    return {
        "model_name": model_name,
        "conf": conf,
        "iou": iou,
        # None means "do not filter"
        "classes": classes if classes and len(classes) < len(config.COCO_CLASSES) else None,
    }


def decode_image(file_bytes: bytes):
    """Bytes -> BGR numpy image, or None if the file is not a valid image."""
    array = np.frombuffer(file_bytes, np.uint8)
    return cv2.imdecode(array, cv2.IMREAD_COLOR)


def run_image_detection(image_bgr, settings: dict):
    """Load the cached model and run detection with the sidebar settings."""
    model = get_model(settings["model_name"])
    return detect_objects(model, image_bgr, settings["conf"], settings["iou"], settings["classes"])


def class_counts(df: pd.DataFrame) -> dict:
    """{'person': 3, 'car': 1} from a detections table."""
    return df["class_name"].value_counts().to_dict() if not df.empty else {}


def count_chart(counts: dict, title: str = "Objects per class"):
    """Plotly bar chart of class counts."""
    data = pd.DataFrame({"class": list(counts.keys()), "count": list(counts.values())})
    fig = px.bar(data, x="class", y="count", title=title, color="class")
    fig.update_layout(showlegend=False)
    return fig


def show_image_results(annotated_rgb, df: pd.DataFrame, inference_ms: float, name: str) -> None:
    """Metrics, table, chart and download buttons (used by image and webcam pages)."""
    st.image(annotated_rgb, caption="Detected objects", width="stretch")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Objects found", len(df))
    c2.metric("Inference time", f"{inference_ms:.0f} ms")
    c3.metric("Avg confidence", f"{df['confidence'].mean():.2f}" if not df.empty else "-")
    c4.metric("Unique classes", df["class_name"].nunique() if not df.empty else 0)

    if df.empty:
        st.warning("No objects detected. Try lowering the confidence threshold.")
        return

    left, right = st.columns(2)
    left.dataframe(df, width="stretch")
    right.plotly_chart(count_chart(class_counts(df)), width="stretch")

    png = io.BytesIO()
    Image.fromarray(annotated_rgb).save(png, format="PNG")
    d1, d2 = st.columns(2)
    d1.download_button("⬇️ Download annotated image (PNG)", png.getvalue(),
                       file_name=f"{name}_detected.png", mime="image/png")
    d2.download_button("⬇️ Download detections (CSV)", df.to_csv(index=False),
                       file_name=f"{name}_detections.csv", mime="text/csv")
