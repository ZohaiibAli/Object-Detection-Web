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
from utils.theme import inject_css, style_fig

def setup_page(title: str, subtitle: str = "", eyebrow: str = "VisionScan", hero: bool = False) -> None:
    """Page config + theme CSS + header. Call first on every page.

    Wrap a word of the title in <em>...</em> to get the italic serif accent.
    """
    st.set_page_config(page_title="VisionScan", page_icon="🎯", layout="wide")
    inject_css()
    box = "hero" if hero else ""
    st.markdown(
        f'<div class="{box}"><span class="eyebrow">{eyebrow}</span>'
        f'<div class="page-title">{title}</div>'
        f'<div class="subtitle">{subtitle}</div></div>',
        unsafe_allow_html=True,
    )


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

    st.sidebar.markdown('<div class="side-title">Detection settings</div>', unsafe_allow_html=True)
    with st.sidebar.container(border=True):
        model_name = st.selectbox("Model", config.MODEL_OPTIONS,
                                  index=config.MODEL_OPTIONS.index(state["model_name"]))
        conf = st.slider("Confidence threshold", 0.05, 0.95, float(state["conf"]), 0.05)
        iou = st.slider("IoU threshold", 0.10, 0.95, float(state["iou"]), 0.05)
        classes = st.multiselect("Classes to detect", config.COCO_CLASSES, default=state["classes"])

    # save back so the values survive when the user switches page
    state.update(model_name=model_name, conf=conf, iou=iou, classes=classes)

    if not classes:
        st.sidebar.warning("No class selected - all classes will be used.")
    st.sidebar.markdown('<div class="side-footer">YOLOv8 · CPU inference<br>Settings are kept across pages</div>',
                        unsafe_allow_html=True)
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
    return style_fig(fig)


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
