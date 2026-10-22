"""Image detection page."""
from pathlib import Path

import streamlit as st

from backend import config
from backend.database import save_record
from utils.ui import (class_counts, decode_image, run_image_detection, setup_page,
                      show_image_results, sidebar_settings)

setup_page("Detect objects in <em>any image</em>", "Upload an image or choose a sample.", eyebrow="Image detection")
settings = sidebar_settings()

uploaded = st.file_uploader("Upload an image", type=config.ALLOWED_IMAGE_TYPES)
samples = sorted(p.name for p in config.SAMPLE_DIR.glob("*") if p.suffix.lower() in (".jpg", ".jpeg", ".png"))
sample_name = st.selectbox("...or pick a sample image", ["(none)"] + samples) if samples else "(none)"

# Work out which image to use
file_bytes, filename = None, None
if uploaded is not None:
    file_bytes, filename = uploaded.getvalue(), uploaded.name
elif sample_name != "(none)":
    file_bytes, filename = (config.SAMPLE_DIR / sample_name).read_bytes(), sample_name

if file_bytes is None:
    st.info("Upload an image or pick a sample to start.")
    st.stop()

image = decode_image(file_bytes)
if image is None:
    st.error("This file could not be read as an image. Please upload a valid JPG, PNG or WEBP.")
    st.stop()

try:
    with st.spinner("Detecting objects..."):
        annotated, df, inference_ms = run_image_detection(image, settings)
except Exception as error:
    st.error(f"Detection failed: {error}")
    st.stop()

original, result = st.columns(2)
original.image(image[:, :, ::-1], caption="Original", width="stretch")
with result:
    show_image_results(annotated, df, inference_ms, Path(filename).stem)

# Save once per distinct run (not on every Streamlit rerun)
run_id = (filename, len(file_bytes), settings["model_name"], settings["conf"], settings["iou"],
          tuple(settings["classes"] or ()))
if st.session_state.get("last_image_run") != run_id:
    save_record("image", filename, settings["model_name"], settings["conf"], len(df),
                inference_ms, class_counts(df))
    st.session_state["last_image_run"] = run_id
