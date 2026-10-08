import math
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="AquaMind AI Prototype",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(180deg, #06121f 0%, #0a1a2a 55%, #0b1622 100%);
            color: #edf7ff;
        }
        [data-testid="stSidebar"] {
            background: #07131f;
            border-right: 1px solid rgba(77, 182, 255, 0.16);
        }
        .block-container {padding-top: 1.3rem; padding-bottom: 2.0rem;}
        h1, h2, h3, h4 {color: #f4fbff !important;}
        .eyebrow {
            color: #67c7ff;
            letter-spacing: .16em;
            font-weight: 700;
            font-size: .75rem;
            text-transform: uppercase;
        }
        .hero-title {
            font-size: 2.45rem;
            line-height: 1.05;
            margin: .2rem 0 .35rem 0;
            font-weight: 800;
        }
        .hero-subtitle {
            color: #b7ccda;
            max-width: 960px;
            font-size: 1.02rem;
        }
        .proto-badge {
            display: inline-block;
            margin-top: .55rem;
            padding: .35rem .65rem;
            border: 1px solid rgba(103,199,255,.35);
            border-radius: 999px;
            color: #9edcff;
            background: rgba(103,199,255,.08);
            font-size: .78rem;
            font-weight: 700;
        }
        .metric-card {
            background: rgba(10, 31, 50, .94);
            border: 1px solid rgba(103,199,255,.15);
            border-radius: 16px;
            padding: 1rem 1.05rem;
            min-height: 116px;
            box-shadow: 0 8px 30px rgba(0,0,0,.16);
        }
        .metric-label {color:#8eacbf; font-size:.78rem; text-transform:uppercase; letter-spacing:.08em;}
        .metric-value {font-size:1.65rem; font-weight:800; margin-top:.3rem; color:#ffffff;}
        .metric-note {color:#a9c0ce; font-size:.78rem; margin-top:.2rem;}
        .panel {
            background: rgba(10, 31, 50, .92);
            border: 1px solid rgba(103,199,255,.15);
            border-radius: 16px;
            padding: 1rem 1.1rem;
            box-shadow: 0 8px 30px rgba(0,0,0,.14);
        }
        .alert-high {
            background: rgba(255, 92, 92, .10);
            border: 1px solid rgba(255, 92, 92, .35);
            border-left: 5px solid #ff6b6b;
            border-radius: 14px;
            padding: 1rem 1.05rem;
        }
        .alert-normal {
            background: rgba(70, 210, 145, .10);
            border: 1px solid rgba(70, 210, 145, .28);
            border-left: 5px solid #46d291;
            border-radius: 14px;
            padding: 1rem 1.05rem;
        }
        .small-muted {color:#94aebf; font-size:.78rem;}
        .flow-step {
            background: rgba(9, 33, 54, .92);
            border: 1px solid rgba(103,199,255,.16);
            border-radius: 14px;
            padding: .8rem .85rem;
            min-height: 92px;
        }
        .flow-num {color:#67c7ff; font-size:.72rem; font-weight:800; letter-spacing:.1em;}
        .flow-title {color:white; font-weight:800; margin-top:.25rem;}
        .flow-copy {color:#9cb5c5; font-size:.76rem; margin-top:.2rem;}
        .footer-note {color:#7893a5; font-size:.72rem; margin-top:1rem;}
        div[data-testid="stMetric"] {
            background: rgba(10,31,50,.88);
            border: 1px solid rgba(103,199,255,.15);
            padding: .8rem;
            border-radius: 14px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Session state
# -----------------------------
if "scenario" not in st.session_state:
    st.session_state.scenario = "Normal operation"
if "seed" not in st.session_state:
    st.session_state.seed = 8

# -----------------------------
# Synthetic network data
# -----------------------------
ZONES = {
    "Zone A-07": {"pressure": 4.7, "flow": 43.0},
    "Zone B-12": {"pressure": 4.4, "flow": 39.0},
    "Zone C-03": {"pressure": 4.9, "flow": 46.0},
}


def generate_data(scenario: str, seed: int = 8) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    points = 90
    end = datetime.now().replace(second=0, microsecond=0)
    times = [end - timedelta(minutes=points - 1 - i) for i in range(points)]
    rows = []

    for zone, cfg in ZONES.items():
        base_p = cfg["pressure"]
        base_f = cfg["flow"]
        pressure = base_p + rng.normal(0, 0.045, points)
        flow = base_f + rng.normal(0, 0.55, points)

        # Add a gentle demand cycle to keep the demo realistic.
        cycle = np.sin(np.linspace(0, 3 * math.pi, points))
        pressure += 0.06 * cycle
        flow += 0.9 * cycle

        if scenario == "Simulated leak" and zone == "Zone B-12":
            start = 58
            pressure[start:] -= np.linspace(0.05, 0.78, points - start)
            flow[start:] += np.linspace(0.2, 7.8, points - start)
        elif scenario == "Pressure surge" and zone == "Zone C-03":
            start = 68
            pulse = np.zeros(points)
            pulse[start:start+7] = np.array([0.2, 0.55, 1.0, 0.72, 0.38, 0.18, 0.06])
            pressure += pulse

        for i in range(points):
            rows.append(
                {
                    "timestamp": times[i],
                    "zone": zone,
                    "pressure_bar": float(pressure[i]),
                    "flow_lps": float(flow[i]),
                    "expected_pressure_bar": base_p,
                    "expected_flow_lps": base_f,
                }
            )

    df = pd.DataFrame(rows)
    return df


def risk_for_row(row: pd.Series) -> tuple[float, str]:
    p_dev = max(0.0, (row["expected_pressure_bar"] - row["pressure_bar"]) / 0.8)
    f_dev = max(0.0, (row["flow_lps"] - row["expected_flow_lps"]) / 8.0)
    score = min(100.0, 100 * (0.58 * p_dev + 0.42 * f_dev))
    if score >= 65:
        level = "HIGH"
    elif score >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"
    return score, level


def build_network_figure(active_zone: str, risk_level: str) -> go.Figure:
    nodes = {
        "Reservoir": (0.0, 1.0),
        "Main Junction": (1.3, 1.0),
        "Zone A-07": (2.7, 1.8),
        "Zone B-12": (2.7, 1.0),
        "Zone C-03": (2.7, 0.2),
    }
    edges = [
        ("Reservoir", "Main Junction"),
        ("Main Junction", "Zone A-07"),
        ("Main Junction", "Zone B-12"),
        ("Main Junction", "Zone C-03"),
    ]

    fig = go.Figure()
    for a, b in edges:
        xa, ya = nodes[a]
        xb, yb = nodes[b]
        fig.add_trace(
            go.Scatter(
                x=[xa, xb],
                y=[ya, yb],
                mode="lines",
                line=dict(color="#2a6f97", width=8),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    xs, ys, labels, colors, sizes = [], [], [], [], []
    for name, (x, y) in nodes.items():
        xs.append(x)
        ys.append(y)
        labels.append(name)
        if name == active_zone and risk_level == "HIGH":
            colors.append("#ff6b6b")
            sizes.append(34)
        elif name == active_zone and risk_level == "MEDIUM":
            colors.append("#ffcc66")
            sizes.append(31)
        elif name == "Reservoir":
            colors.append("#67c7ff")
            sizes.append(32)
        else:
            colors.append("#46d291")
            sizes.append(28)

    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode="markers+text",
            text=labels,
            textposition="bottom center",
            textfont=dict(color="#d9eef9", size=13),
            marker=dict(color=colors, size=sizes, line=dict(color="#0a1a2a", width=3)),
            hovertemplate="%{text}<extra></extra>",
            showlegend=False,
        )
    )
    fig.update_layout(
        height=365,
        margin=dict(l=10, r=10, t=10, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False, range=[-0.35, 3.25]),
        yaxis=dict(visible=False, range=[-0.2, 2.15]),
    )
    return fig


def build_timeseries_figure(zone_df: pd.DataFrame, metric: str, expected_col: str, y_title: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=zone_df["timestamp"],
            y=zone_df[metric],
            mode="lines",
            name="Measured",
            line=dict(color="#67c7ff", width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=zone_df["timestamp"],
            y=zone_df[expected_col],
            mode="lines",
            name="Expected",
            line=dict(color="#7f95a3", width=2, dash="dash"),
        )
    )
    fig.update_layout(
        height=270,
        margin=dict(l=5, r=5, t=5, b=5),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#cfe3ee"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(gridcolor="rgba(130,170,195,.12)", title=y_title),
    )
    return fig


# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.markdown("### Demo controls")
st.sidebar.caption("Use these controls during rehearsal. The pitch slide should use a screenshot so your presentation does not depend on a live demo.")

if st.sidebar.button("▶ Simulate leak in Zone B-12", use_container_width=True):
    st.session_state.scenario = "Simulated leak"
if st.sidebar.button("⚡ Simulate pressure surge", use_container_width=True):
    st.session_state.scenario = "Pressure surge"
if st.sidebar.button("↺ Reset to normal", use_container_width=True):
    st.session_state.scenario = "Normal operation"

st.sidebar.markdown("---")
selected_zone = st.sidebar.selectbox("Inspect zone", list(ZONES.keys()), index=1)
st.sidebar.markdown("**Current scenario**")
st.sidebar.info(st.session_state.scenario)
st.sidebar.caption("All readings in this prototype are synthetic and are not field-validation results.")

# -----------------------------
# Data + analytics
# -----------------------------
df = generate_data(st.session_state.scenario, st.session_state.seed)
zone_df = df[df["zone"] == selected_zone].copy()
latest = zone_df.iloc[-1]
risk_score, risk_level = risk_for_row(latest)

# Global active anomaly zone for network schematic
latest_rows = df.sort_values("timestamp").groupby("zone", as_index=False).tail(1)
zone_risks = {}
for _, row in latest_rows.iterrows():
    score, level = risk_for_row(row)
    zone_risks[row["zone"]] = (score, level)
active_zone = max(zone_risks, key=lambda z: zone_risks[z][0])
active_score, active_level = zone_risks[active_zone]

pressure_delta = latest["pressure_bar"] - latest["expected_pressure_bar"]
flow_delta = latest["flow_lps"] - latest["expected_flow_lps"]

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="eyebrow">AquaMind AI · Water Network Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Predictive Water Network Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">A visual prototype of the AquaMind workflow: pressure and flow sensing → anomaly analytics → operator action. Built for the DMZ pitch using simulated hydraulic data.</div>',
    unsafe_allow_html=True,
)
st.markdown('<span class="proto-badge">PROTOTYPE · SYNTHETIC DATA · NOT FIELD-VALIDATED</span>', unsafe_allow_html=True)
st.write("")

# -----------------------------
# KPI cards
# -----------------------------
cols = st.columns(4)
metrics = [
    ("Network status", "Attention" if active_level != "LOW" else "Stable", f"Scenario: {st.session_state.scenario}"),
    ("Highest leak risk", f"{active_score:.0f}%", f"{active_zone} · {active_level}"),
    ("Pressure", f"{latest['pressure_bar']:.2f} bar", f"Δ {pressure_delta:+.2f} bar vs expected"),
    ("Flow rate", f"{latest['flow_lps']:.1f} L/s", f"Δ {flow_delta:+.1f} L/s vs expected"),
]
for c, (label, value, note) in zip(cols, metrics):
    c.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# -----------------------------
# Main row: network + alert
# -----------------------------
left, right = st.columns([1.55, 1.0])
with left:
    st.markdown("### Network overview")
    st.plotly_chart(build_network_figure(active_zone, active_level), use_container_width=True, config={"displayModeBar": False})

with right:
    st.markdown("### AquaMind insight")
    if active_level == "HIGH":
        st.markdown(
            f"""
            <div class="alert-high">
                <b>Potential leak signature detected</b><br><br>
                <b>Zone:</b> {active_zone}<br>
                <b>Risk level:</b> {active_level}<br>
                <b>Prototype risk score:</b> {active_score:.0f}%<br><br>
                <b>Recommended operator action:</b><br>
                Inspect the affected sector, verify pressure/flow readings, and prepare targeted isolation if the anomaly persists.
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif active_level == "MEDIUM":
        st.warning(f"Hydraulic deviation detected in {active_zone}. Continue monitoring and verify sensor readings.")
    else:
        st.markdown(
            """
            <div class="alert-normal">
                <b>No critical anomaly detected</b><br><br>
                Pressure and flow remain within the prototype operating envelope. Continue continuous monitoring.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.markdown("#### What the prototype demonstrates")
    st.markdown(
        """
        - Real-time-style monitoring of pressure and flow signals
        - Zone-level hydraulic anomaly detection
        - Risk prioritization for operators
        - A clear path from **data → analytics → action**
        """
    )

# -----------------------------
# Signal charts
# -----------------------------
st.markdown("### Signal behavior")
c1, c2 = st.columns(2)
with c1:
    st.caption(f"Pressure · {selected_zone}")
    st.plotly_chart(
        build_timeseries_figure(zone_df, "pressure_bar", "expected_pressure_bar", "bar"),
        use_container_width=True,
        config={"displayModeBar": False},
    )
with c2:
    st.caption(f"Flow · {selected_zone}")
    st.plotly_chart(
        build_timeseries_figure(zone_df, "flow_lps", "expected_flow_lps", "L/s"),
        use_container_width=True,
        config={"displayModeBar": False},
    )

# -----------------------------
# Data -> analytics -> action flow
# -----------------------------
st.markdown("### AquaMind workflow")
flow_cols = st.columns(5)
flow_items = [
    ("01", "Sensing", "Pressure and flow signals from network sensors."),
    ("02", "Ingestion", "Clean, normalize and validate incoming data."),
    ("03", "Analytics", "Detect abnormal hydraulic patterns and rank risk."),
    ("04", "Decision", "Translate signals into an operator recommendation."),
    ("05", "Action", "Verify, inspect and respond before the issue escalates."),
]
for col, (num, title, copy) in zip(flow_cols, flow_items):
    col.markdown(
        f"""
        <div class="flow-step">
            <div class="flow-num">{num}</div>
            <div class="flow-title">{title}</div>
            <div class="flow-copy">{copy}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="footer-note">Prototype note: this interface visualizes the intended AquaMind AI workflow using synthetic data. It does not claim field-tested accuracy, validated leak-localization precision, or production response latency. Those are pilot-validation milestones.</div>',
    unsafe_allow_html=True,
)
