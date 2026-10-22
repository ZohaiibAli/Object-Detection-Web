"""Video detection page."""
import tempfile
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from backend import config
from backend.database import save_record
from backend.video_utils import process_video
from utils.theme import style_fig
from utils.ui import count_chart, get_model, setup_page, sidebar_settings

setup_page("Detect objects in <em>video</em>", "Upload a short video and detect objects in every frame.", eyebrow="Video detection")
settings = sidebar_settings()

st.info(f"To stay fast on the free cloud tier only the first {config.MAX_VIDEO_SECONDS} seconds "
        f"(max {config.MAX_VIDEO_FRAMES} frames) are processed.")

uploaded = st.file_uploader("Upload a video", type=config.ALLOWED_VIDEO_TYPES)
frame_skip = st.slider("Detect every Nth frame (higher = faster)", 1, 10, config.DEFAULT_FRAME_SKIP)

if uploaded is not None and st.button("▶️ Process video", type="primary"):
    # temp files are removed at the end, even if processing fails
    suffix = Path(uploaded.name).suffix
    with tempfile.TemporaryDirectory() as folder:
        input_path = Path(folder) / f"input{suffix}"
        output_path = Path(folder) / "output.mp4"
        input_path.write_bytes(uploaded.getvalue())

        progress = st.progress(0.0, text="Processing video...")
        try:
            model = get_model(settings["model_name"])
            summary = process_video(model, input_path, output_path, settings["conf"], settings["iou"],
                                    settings["classes"], frame_skip, progress.progress)
            video_bytes = output_path.read_bytes()
        except Exception as error:
            progress.empty()
            st.error(f"Could not process this video: {error}")
            st.stop()
        progress.empty()

    # keep results in session_state so they stay on screen after button clicks
    st.session_state["video_result"] = {"summary": summary, "video": video_bytes, "name": uploaded.name}
    save_record("video", uploaded.name, settings["model_name"], settings["conf"],
                summary["total_detections"], 0.0, summary["class_counts"])

result = st.session_state.get("video_result")
if result:
    summary = result["summary"]
    st.video(result["video"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Frames processed", summary["frames_processed"])
    c2.metric("Average FPS", summary["average_fps"])
    c3.metric("Total detections", summary["total_detections"])
    c4.metric("Unique classes", len(summary["class_counts"]))

    if summary["total_detections"] == 0:
        st.warning("No objects detected in this video. Try lowering the confidence threshold.")
    else:
        left, right = st.columns(2)
        per_frame = pd.DataFrame({"frame": range(len(summary["detections_per_frame"])),
                                  "detections": summary["detections_per_frame"]})
        left.plotly_chart(style_fig(px.line(per_frame, x="frame", y="detections", title="Detections per processed frame")),
                          width="stretch")
        right.plotly_chart(count_chart(summary["class_counts"], "Detections per class"),
                           width="stretch")

    summary_csv = pd.DataFrame(list(summary["class_counts"].items()), columns=["class_name", "count"])
    d1, d2 = st.columns(2)
    d1.download_button("⬇️ Download processed video", result["video"],
                       file_name=f"{Path(result['name']).stem}_detected.mp4", mime="video/mp4")
    d2.download_button("⬇️ Download summary (CSV)", summary_csv.to_csv(index=False),
                       file_name="video_summary.csv", mime="text/csv")
elif uploaded is None:
    st.info("Upload a video (mp4, avi, mov, mkv) to start.")
