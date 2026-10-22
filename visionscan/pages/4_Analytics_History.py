"""Analytics and history page."""
import json

import pandas as pd
import plotly.express as px
import streamlit as st

from backend.database import clear_history, get_history
from utils.theme import style_fig
from utils.ui import setup_page

setup_page("Your detection <em>analytics</em>", "Everything detected so far.", eyebrow="Analytics & history")

history = get_history()
if history.empty:
    st.info("No history yet. Run a detection first.")
    st.stop()

# Add up the per-class counts stored as JSON in each row
class_totals = {}
for text in history["class_counts_json"].dropna():
    for name, count in json.loads(text).items():
        class_totals[name] = class_totals.get(name, 0) + count

# Summary metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total runs", len(history))
c2.metric("Total objects", int(history["num_objects"].sum()))
image_times = history[history["inference_ms"] > 0]["inference_ms"]
c3.metric("Avg inference time", f"{image_times.mean():.0f} ms" if not image_times.empty else "-")
c4.metric("Most detected class", max(class_totals, key=class_totals.get) if class_totals else "-")

# Charts
history["date"] = pd.to_datetime(history["timestamp"]).dt.date
left, middle, right = st.columns(3)

runs_per_day = history.groupby("date").size().reset_index(name="runs")
left.plotly_chart(style_fig(px.line(runs_per_day, x="date", y="runs", markers=True, title="Runs over time")),
                  width="stretch")

per_source = history.groupby("source_type")["num_objects"].sum().reset_index()
middle.plotly_chart(style_fig(px.bar(per_source, x="source_type", y="num_objects", color="source_type",
                                     title="Objects per source type")), width="stretch")

top = sorted(class_totals.items(), key=lambda item: item[1], reverse=True)[:10]
top_df = pd.DataFrame(top, columns=["class", "count"])
right.plotly_chart(style_fig(px.bar(top_df, x="class", y="count", color="class", title="Top 10 classes")),
                   width="stretch")

# History table
st.subheader("History")
choice = st.selectbox("Filter by source", ["all", "image", "video", "webcam"])
shown = history if choice == "all" else history[history["source_type"] == choice]
shown = shown.drop(columns=["date"])
st.dataframe(shown, width="stretch")
st.download_button("⬇️ Export CSV", shown.to_csv(index=False), file_name="history.csv", mime="text/csv")

# Clear history with confirmation
st.subheader("Danger zone")
confirm = st.checkbox("Yes, I want to delete all history")
if st.button("🗑️ Clear history", disabled=not confirm):
    clear_history()
    st.rerun()
