"""VisionScan - Home page. Run with: streamlit run app.py"""
import streamlit as st

from backend.database import get_history, init_db
from utils.ui import setup_page

setup_page("🎯 VisionScan", "Real-time object detection with YOLOv8 - upload an image, a video, or use your webcam.")
init_db()

# Feature cards
col1, col2, col3 = st.columns(3)
col1.markdown('<div class="card"><h3>🖼️ Image</h3>Upload a photo or pick a sample. '
              'See boxes, labels and confidence scores.</div>', unsafe_allow_html=True)
col2.markdown('<div class="card"><h3>🎬 Video</h3>Process a short clip frame by frame and '
              'watch the annotated result.</div>', unsafe_allow_html=True)
col3.markdown('<div class="card"><h3>📷 Webcam</h3>Take a photo with your camera and '
              'detect objects instantly.</div>', unsafe_allow_html=True)

# How it works
st.subheader("How it works")
s1, s2, s3, s4 = st.columns(4)
s1.markdown("**1. Upload**  \nChoose an image, video or camera shot.")
s2.markdown("**2. YOLOv8 inference**  \nThe model looks at the picture once.")
s3.markdown("**3. Boxes drawn**  \nEach object gets a box, label and score.")
s4.markdown("**4. Analytics**  \nResults are saved and charted.")

# Stats from the database
history = get_history()
st.subheader("Your stats")
m1, m2 = st.columns(2)
m1.metric("Total runs", len(history))
m2.metric("Total detections", int(history["num_objects"].sum()) if not history.empty else 0)

st.info("👈 Use the sidebar to open a detection page.")
