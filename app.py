import streamlit as st
import pandas as pd
from detection.analytics import make_synthetic_data, analyze_records, load_csv
from detection.video import process_video
from modes.crowd import crowd_summary
from modes.tourism import tourism_summary

st.set_page_config(page_title="AI-CCTV | Command Center", page_icon="📹", layout="wide")
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root{--ink:#17243b;--muted:#718096;--teal:#0f9d91;--line:#e5ebf2;--canvas:#f5f8fc}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.stApp{background:var(--canvas);color:var(--ink)}
[data-testid="stHeader"]{background:rgba(245,248,252,.88)}
[data-testid="stSidebar"]{background:#fff;border-right:1px solid var(--line)}
.block-container{max-width:1500px;padding-top:1.6rem;padding-bottom:2.6rem}
h1,h2,h3{font-family:'Space Grotesk',sans-serif!important;color:var(--ink);letter-spacing:-.025em}
h1{font-size:2.05rem!important} h2{font-size:1.35rem!important} h3{font-size:1.05rem!important}
.hero{background:linear-gradient(120deg,#132b45 0%,#19465c 58%,#0f817b 100%);border-radius:22px;padding:27px 30px;color:#fff;margin-bottom:22px;box-shadow:0 12px 30px rgba(22,49,74,.1)}
.hero-eyebrow{color:#9ce7df;text-transform:uppercase;letter-spacing:.15em;font-size:.72rem;font-weight:700;margin-bottom:8px}
.hero-title{color:#fff;font-family:'Space Grotesk',sans-serif;font-size:1.9rem;line-height:1.15;font-weight:700;margin-bottom:8px}
.hero-copy{color:#d8e8f0;font-size:.96rem;max-width:780px;line-height:1.55}
.hero-pill{display:inline-block;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.09);color:#effdfb;border-radius:999px;padding:6px 11px;font-size:.75rem;font-weight:600;margin:12px 6px 0 0}
.section-kicker{color:#087f78;font-size:.72rem;text-transform:uppercase;letter-spacing:.12em;font-weight:700;margin-bottom:4px}
.section-note{color:var(--muted);font-size:.88rem;margin-top:-7px;margin-bottom:12px}
div[data-testid="stMetric"]{background:#fff;border:1px solid var(--line);border-radius:16px;padding:17px 19px;box-shadow:0 4px 14px rgba(25,48,74,.035)}
div[data-testid="stMetricLabel"]{color:#697b90;font-size:.82rem;font-weight:600}
div[data-testid="stMetricValue"]{color:var(--ink);font-family:'Space Grotesk',sans-serif;font-size:1.85rem}
div[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:13px;overflow:hidden}
div[data-testid="stAlert"]{border-radius:12px}
.sidebar-brand{background:#142d47;color:#fff;border-radius:15px;padding:16px;margin-bottom:20px}
.sidebar-brand small{color:#9ce7df;text-transform:uppercase;letter-spacing:.13em;font-weight:700;font-size:.66rem}
.sidebar-brand strong{display:block;font-family:'Space Grotesk',sans-serif;font-size:1.15rem;margin-top:5px}
.sidebar-brand span{display:block;color:#d0dfe9;font-size:.78rem;margin-top:4px}
.info-strip{border:1px solid #d9e8ee;background:#f0f8fa;border-radius:12px;padding:12px 15px;color:#34546a;font-size:.85rem}
.footer-note{border-top:1px solid var(--line);padding-top:15px;margin-top:28px;color:#7b8a9d;font-size:.78rem}
.stButton>button[kind="primary"]{background:var(--teal);border-color:var(--teal);border-radius:10px;font-weight:700}
.stButton>button[kind="primary"]:hover{background:#087f78;border-color:#087f78}
@media(max-width:768px){.hero{padding:22px}.hero-title{font-size:1.55rem}.block-container{padding-top:1rem}}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('''<div class="sidebar-brand"><small>Vision • Analytics • Safety</small><strong>AI-CCTV Command Center</strong><span>Prototype monitoring workspace</span></div>''', unsafe_allow_html=True)
    st.markdown("### Workspace settings")
    mode = st.radio("Monitoring mode", ["Crowd Management", "Tourism / Heritage"])
    source = st.radio("Data input", ["Synthetic dataset", "Upload CSV", "Upload video"])
    st.divider()
    st.markdown("### Alert configuration")
    threshold = st.slider("Crowd count threshold", 5, 500, 30, 5)
    st.caption("A record is flagged when its count is greater than or equal to this value.")
    st.divider()
    st.caption("Prototype only • No live CCTV connection is configured.")

mode_label = "CROWD OPERATIONS" if mode == "Crowd Management" else "TOURISM & HERITAGE"
st.markdown(f'''<div class="hero"><div class="hero-eyebrow">AI monitoring workspace · {mode_label}</div><div class="hero-title">See the crowd. Understand the pattern.</div><div class="hero-copy">Explore people-count trends, compare monitored zones, and review threshold alerts from generated records, an uploaded CSV, or an uploaded video.</div><span class="hero-pill">● Analytics dashboard</span><span class="hero-pill">YOLOv8 video option</span><span class="hero-pill">Human-reviewed alerts</span></div>''', unsafe_allow_html=True)
st.markdown('<div class="section-kicker">Monitoring overview</div>', unsafe_allow_html=True)
st.markdown(f"## {mode}")
st.markdown('<div class="section-note">Choose an input in the sidebar. Results below update for that input.</div>', unsafe_allow_html=True)

def show_analytics(df: pd.DataFrame, is_synthetic: bool = False):
    result = analyze_records(df, threshold)
    summary = crowd_summary(result) if mode == "Crowd Management" else tourism_summary(result)
    alert_rows = df[df["people_count"] >= threshold].copy()
    alert_rows["alert_level"] = "HIGH"
    c1, c2, c3 = st.columns(3)
    c1.metric("Total records", f"{len(df):,}")
    c2.metric("Average people count", f"{df['people_count'].mean():.1f}")
    c3.metric("Records at / above threshold", f"{len(alert_rows):,}")
    st.markdown("### Crowd activity")
    st.markdown('<div class="section-note">Each point represents a record in the selected dataset—not necessarily a unique person.</div>', unsafe_allow_html=True)
    chart_df = df.copy()
    if "timestamp" in chart_df.columns:
        chart_df["timestamp"] = pd.to_datetime(chart_df["timestamp"], errors="coerce")
        chart_df = chart_df.dropna(subset=["timestamp"]).sort_values("timestamp")
        if not chart_df.empty:
            st.line_chart(chart_df.set_index("timestamp")["people_count"], use_container_width=True)
        else:
            st.info("No usable timestamps were found, so the trend chart cannot be displayed.")
    else:
        st.line_chart(df["people_count"], use_container_width=True)
    tab_zone, tab_alerts, tab_data, tab_summary = st.tabs(["Zone summary", "Alert center", "Dataset preview", "Mode insights"])
    with tab_zone:
        st.markdown("#### Zone-wise crowd overview")
        st.caption("Aggregated values from the current dataset.")
        st.dataframe(result, use_container_width=True, hide_index=True)
    with tab_alerts:
        st.markdown("#### Threshold alert records")
        if alert_rows.empty:
            st.success("No records meet the selected threshold.")
        else:
            st.dataframe(alert_rows[["timestamp", "zone", "people_count", "alert_level"]], use_container_width=True, hide_index=True)
            st.caption("These are threshold-based flags for review, not confirmation of an unsafe situation.")
    with tab_data:
        st.markdown("#### Input records")
        st.dataframe(df.head(100), use_container_width=True, hide_index=True)
        if is_synthetic:
            st.info("Synthetic records are generated examples, not real CCTV observations.")
        st.download_button("Download records as CSV", data=df.to_csv(index=False).encode("utf-8"), file_name="crowd_records.csv", mime="text/csv")
    with tab_summary:
        st.markdown("#### Mode-specific summary")
        st.write(summary)
    if is_synthetic:
        st.markdown('<div class="info-strip">Synthetic data is useful for testing the dashboard workflow. It does not validate real-world crowd-detection accuracy.</div>', unsafe_allow_html=True)

if source == "Synthetic dataset":
    with st.expander("Synthetic dataset settings", expanded=True):
        settings1, settings2 = st.columns(2)
        with settings1:
            rows = st.slider("Number of sample records", 20, 1000, 200, 20)
        with settings2:
            seed = st.number_input("Random seed", min_value=0, max_value=99999, value=42)
        st.caption("Keeping the same seed and record count makes the random component reproducible.")
    df = make_synthetic_data(rows=int(rows), seed=int(seed))
    show_analytics(df, is_synthetic=True)
elif source == "Upload CSV":
    st.markdown("### Import crowd-count data")
    st.markdown('<div class="section-note">Required column: people_count. Optional columns: timestamp and zone.</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Choose a CSV file", type=["csv"], help="Upload tabular crowd-count data. This does not upload video footage.")
    if uploaded is not None:
        try:
            df = load_csv(uploaded)
            show_analytics(df)
        except Exception as e:
            st.error(f"Could not process this CSV: {e}")
    else:
        st.markdown('<div class="info-strip">Upload a compatible CSV to view the analytics dashboard.</div>', unsafe_allow_html=True)