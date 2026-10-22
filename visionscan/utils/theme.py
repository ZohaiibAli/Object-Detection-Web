"""Purple light/dark look for VisionScan (CSS + chart colors)."""
import streamlit as st

# One palette per theme. The CSS below reads these as variables.
LIGHT = {
    "bg": "linear-gradient(180deg, #e6effb 0%, #ecebfd 35%, #d8d4fb 100%)",
    "sidebar": "rgba(255,255,255,0.65)",
    "card": "rgba(255,255,255,0.78)",
    "border": "rgba(99,82,214,0.16)",
    "shadow": "0 8px 28px rgba(79,70,229,0.12)",
    "text": "#1e1b4b",
    "muted": "#5b5896",
    "accent": "#5b3df5",
    "pill": "rgba(124,58,237,0.12)",
    "grid": "rgba(30,27,75,0.10)",
}
DARK = {
    "bg": "linear-gradient(180deg, #14123a 0%, #1b1950 55%, #261f72 100%)",
    "sidebar": "rgba(20,18,58,0.85)",
    "card": "rgba(38,34,104,0.55)",
    "border": "rgba(167,139,250,0.22)",
    "shadow": "0 8px 28px rgba(0,0,0,0.35)",
    "text": "#ece9ff",
    "muted": "#aaa6dc",
    "accent": "#a78bfa",
    "pill": "rgba(167,139,250,0.16)",
    "grid": "rgba(236,233,255,0.12)",
}
CHART_COLORS = ["#6d4aff", "#a78bfa", "#ec4899", "#38bdf8", "#f59e0b", "#34d399", "#818cf8", "#f472b6"]

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Instrument+Serif:ital@0;1&display=swap');

html, body, .stApp, p, label, li, h1, h2, h3, h4, button, input, textarea,
[data-testid="stMetricValue"], [data-testid="stSidebarNav"] span:not([data-testid="stIconMaterial"]) {
    font-family: 'Plus Jakarta Sans', sans-serif;
}
[data-testid="stIconMaterial"] { font-family: 'Material Symbols Rounded' !important; }
.stApp { background: %(bg)s; background-attachment: fixed; color: %(text)s; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2.2rem; max-width: 1150px; }

h1, h2, h3, h4, .stMarkdown, label, p, li { color: %(text)s; }
h2, h3 { font-weight: 700; letter-spacing: -0.01em; }

/* sidebar */
section[data-testid="stSidebar"] {
    background: %(sidebar)s; backdrop-filter: blur(14px);
    border-right: 1px solid %(border)s;
}

/* sidebar: brand, nav pills, settings card */
[data-testid="stSidebarNav"]::before {
    content: "VisionScan"; display: block; padding: 0.4rem 1rem 1rem;
    font-size: 1.45rem; font-weight: 800; letter-spacing: -0.02em;
    background: linear-gradient(90deg, #5b3df5, #c026d3); -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
[data-testid="stSidebarNav"] ul { gap: 0.2rem; padding: 0 0.4rem; }
[data-testid="stSidebarNav"] a {
    border-radius: 999px; padding: 0.45rem 1rem; transition: background 0.15s;
}
[data-testid="stSidebarNav"] a:hover { background: %(pill)s; }
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    box-shadow: 0 6px 16px rgba(99,66,235,0.35);
}
[data-testid="stSidebarNav"] a[aria-current="page"] p { color: #fff !important; font-weight: 600; }
/* the entry file is called "app"; show it as "Home" */
[data-testid="stSidebarNav"] li:first-child a p { font-size: 0 !important; }
[data-testid="stSidebarNav"] li:first-child a p::after { content: "Home"; font-size: 1rem; }
.side-title { font-size: 0.75rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;
    color: %(muted)s; margin: 0.8rem 0 0.4rem 0.2rem; }
section[data-testid="stSidebar"] div[data-testid="stVerticalBlockBorderWrapper"] {
    background: %(card)s; border: 1px solid %(border)s; border-radius: 18px; box-shadow: %(shadow)s;
}
.side-footer { margin-top: 1rem; padding: 0.7rem 0.9rem; border-radius: 14px; background: %(pill)s;
    color: %(muted)s; font-size: 0.78rem; line-height: 1.5; text-align: center; }

/* headline with an italic serif accent, like the reference design */
.eyebrow {
    display: inline-block; padding: 0.3rem 0.9rem; border-radius: 999px;
    background: %(pill)s; color: %(accent)s; font-size: 0.8rem; font-weight: 600;
}
.page-title { font-size: 2.7rem; font-weight: 700; line-height: 1.12; letter-spacing: -0.02em;
    margin: 0.6rem 0 0.3rem; color: %(text)s; }
.page-title em { font-family: 'Instrument Serif', serif; font-weight: 400; font-style: italic; }
.subtitle { font-size: 1.05rem; color: %(muted)s; margin-bottom: 1.4rem; max-width: 46rem; }
.hero { text-align: center; padding: 1.5rem 0 1rem; }
.hero .page-title { font-size: 3.4rem; }
.hero .subtitle { margin-left: auto; margin-right: auto; }

/* cards */
.card, div[data-testid="stMetric"], div[data-testid="stExpander"], div[data-testid="stFileUploader"] section,
div[data-testid="stDataFrame"], div[data-testid="stPlotlyChart"] {
    background: %(card)s; border: 1px solid %(border)s; border-radius: 18px;
    box-shadow: %(shadow)s; backdrop-filter: blur(10px);
}
.card { padding: 1.3rem 1.5rem; height: 100%%; }
.card h3 { margin: 0 0 0.3rem; padding: 0; font-size: 1.25rem; }
[data-testid="stPageLink"] a { justify-content: center; white-space: nowrap; }
.card .icon { font-size: 1.6rem; width: 2.8rem; height: 2.8rem; display: flex; align-items: center;
    justify-content: center; border-radius: 14px; background: %(pill)s; margin-bottom: 0.7rem; }
div[data-testid="stMetric"] { padding: 0.9rem 1.1rem; }
div[data-testid="stMetricValue"] { color: %(accent)s; font-weight: 700; }
div[data-testid="stMetricLabel"] p { color: %(muted)s; }
div[data-testid="stPlotlyChart"], div[data-testid="stDataFrame"] { padding: 0.4rem; overflow: hidden; }

.step-num { display: inline-flex; width: 2rem; height: 2rem; border-radius: 50%%; align-items: center;
    justify-content: center; background: linear-gradient(135deg, #4f46e5, #8b5cf6); color: #fff;
    font-weight: 700; margin-bottom: 0.5rem; }

/* pill buttons */
.stButton > button, .stDownloadButton > button, .stLinkButton a, [data-testid="stPageLink"] a {
    border-radius: 999px; font-weight: 600; padding: 0.5rem 1.4rem;
    border: 1px solid %(border)s; background: %(card)s; color: %(text)s;
}
.stButton > button[kind="primary"], .stDownloadButton > button, [data-testid="stPageLink"] a {
    background: linear-gradient(135deg, #4f46e5, #7c3aed); color: #fff; border: none;
    box-shadow: 0 6px 18px rgba(99,66,235,0.35);
}
.stButton > button:hover, .stDownloadButton > button:hover, [data-testid="stPageLink"] a:hover {
    transform: translateY(-1px); filter: brightness(1.08);
}
.stDownloadButton > button p, [data-testid="stPageLink"] a p { color: #fff !important; }

/* inputs, alerts, progress */
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
    border-radius: 12px; background: %(card)s; border-color: %(border)s;
}
div[data-testid="stAlert"] { border-radius: 14px; border: 1px solid %(border)s; }
div[data-testid="stImage"] img { border-radius: 16px; box-shadow: %(shadow)s; }
video { border-radius: 16px; }
</style>
"""


def current_palette() -> dict:
    """Pick the light or dark palette from the active Streamlit theme."""
    try:
        return DARK if st.context.theme.type == "dark" else LIGHT
    except Exception:
        return LIGHT


def inject_css() -> None:
    st.markdown(CSS % current_palette(), unsafe_allow_html=True)


def style_fig(fig):
    """Make a Plotly figure match the current theme."""
    palette = current_palette()
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color=palette["text"]),
        colorway=CHART_COLORS, margin=dict(l=20, r=20, t=50, b=20),
    )
    fig.update_xaxes(gridcolor=palette["grid"], zerolinecolor=palette["grid"])
    fig.update_yaxes(gridcolor=palette["grid"], zerolinecolor=palette["grid"])
    return fig
