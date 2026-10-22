"""VisionScan - Home page. Run with: streamlit run app.py"""
import streamlit as st

from backend.database import get_history, init_db
from utils.ui import setup_page

setup_page("Object detection made simple <em>for everyone</em>",
           "Upload an image, a video, or use your webcam. YOLOv8 finds the objects, "
           "draws the boxes and keeps analytics of every run.",
           eyebrow="Powered by YOLOv8", hero=True)
init_db()

# Call-to-action buttons
_, b1, b2, b3, _ = st.columns([0.4, 1, 1, 1, 0.4])
b1.page_link("pages/1_Image_Detection.py", label="Try an image", icon="🖼️")
b2.page_link("pages/2_Video_Detection.py", label="Try a video", icon="🎬")
b3.page_link("pages/3_Webcam_Detection.py", label="Use webcam", icon="📷")

st.write("")

# Stats from the database
history = get_history()
m1, m2, m3 = st.columns(3)
m1.metric("Total runs", len(history))
m2.metric("Total detections", int(history["num_objects"].sum()) if not history.empty else 0)
m3.metric("Classes supported", 80)

st.write("")

# Feature cards
col1, col2, col3 = st.columns(3)
col1.markdown('<div class="card"><div class="icon">🖼️</div><h3>Image</h3>Upload a photo or pick a '
              'sample. See boxes, labels and confidence scores.</div>', unsafe_allow_html=True)
col2.markdown('<div class="card"><div class="icon">🎬</div><h3>Video</h3>Process a short clip frame '
              'by frame and watch the annotated result.</div>', unsafe_allow_html=True)
col3.markdown('<div class="card"><div class="icon">📷</div><h3>Webcam</h3>Take a photo with your '
              'camera and detect objects instantly.</div>', unsafe_allow_html=True)

# How it works
st.write("")
st.markdown('<div class="page-title" style="font-size:2rem">How it <em>works</em></div>', unsafe_allow_html=True)
steps = [("Upload", "Choose an image, video or camera shot."),
         ("YOLOv8 inference", "The model looks at the picture once."),
         ("Boxes drawn", "Each object gets a box, label and score."),
         ("Analytics", "Results are saved and charted.")]
for column, (number, (name, text)) in zip(st.columns(4), enumerate(steps, start=1)):
    column.markdown(f'<div class="card"><div class="step-num">{number}</div><br><b>{name}</b><br>{text}</div>',
                    unsafe_allow_html=True)
