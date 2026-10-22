"""Webcam detection page (uses a photo taken in the browser)."""
import streamlit as st

from backend.database import save_record
from utils.ui import (class_counts, decode_image, run_image_detection, setup_page,
                      show_image_results, sidebar_settings)

setup_page("Detect objects with your <em>webcam</em>", "Take a photo with your camera and detect objects in it.", eyebrow="Webcam detection")
settings = sidebar_settings()

st.markdown("1. Allow camera access in your browser.  \n"
            "2. Click **Take Photo**.  \n"
            "3. The detection result appears below.")

photo = st.camera_input("Take a photo")
if photo is None:
    st.stop()

image = decode_image(photo.getvalue())
if image is None:
    st.error("The photo could not be read. Please try again.")
    st.stop()

try:
    with st.spinner("Detecting objects..."):
        annotated, df, inference_ms = run_image_detection(image, settings)
except Exception as error:
    st.error(f"Detection failed: {error}")
    st.stop()

show_image_results(annotated, df, inference_ms, "webcam")

# Save once per photo / settings combination
run_id = (len(photo.getvalue()), settings["model_name"], settings["conf"], settings["iou"],
          tuple(settings["classes"] or ()))
if st.session_state.get("last_webcam_run") != run_id:
    save_record("webcam", "webcam_photo", settings["model_name"], settings["conf"], len(df),
                inference_ms, class_counts(df))
    st.session_state["last_webcam_run"] = run_id
