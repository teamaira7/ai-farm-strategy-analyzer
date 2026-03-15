# app.py — AI Farm Strategy Advisor (Streamlit)
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from simulation import FarmConditions, EconomicFactors, Strategy, compare_strategies, CROP_YIELD_PARAMS
from utils import build_comparison_table, recommend_strategy, format_currency, format_percent, CROP_DEFAULTS

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Farm Strategy Advisor",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
body { font-family: 'Inter', sans-serif; }
.main-header { 
    background: linear-gradient(135deg,#1a5c2e,#4caf7a); 
    padding: 2rem 2.5rem; 
    border-radius: 16px; color:white;
}
.main-header h1 { font-size:2.4rem; margin:0; font-weight:700; }
.main-header p { margin:0.4rem 0 0; opacity:0.88; font-size:1.05rem; }

.metric-card {
    background:#f8fdf9; border:1px solid #d4eadb; border-radius:12px;
    padding:1.1rem 1.4rem; text-align:center; margin-bottom:1rem;
}
.metric-card .value { font-size:1.6rem; font-weight:700; color:#1a5c2e; }
.metric-card .label { font-size:0.9rem; color:#555; margin-top:0.2rem; }

.recommend-box { background: linear-gradient(135deg,#fff9e6,#fff3cd);
    border:2px solid #f0c040; border-radius:14px; padding:1.4rem 1.8rem; margin-top:1rem;
}
.recommend-box h3 { color:#7a5200; margin:0 0 0.3rem; }

.section-title { font-size:1.25rem; font-weight:600; color:#1a5c2e;
    border-left:4px solid #2d8a4e; padding-left:0.75rem; margin:1.5rem 0 0.8rem;
}

.stSlider > div > div > div { background: #2d8a4e !important; }
div[data-testid="stSidebar"] { background:#f4fbf6; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🌾 AI Farm Strategy Advisor</h1>
    <p>Monte Carlo Simulation · Compare strategies under uncertainty · Make informed decisions</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar: Inputs ───────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/farm.png", width=60)
    st.title("⚙️ Farm Config")

    # Collapsible sections for cleaner UX
    with st.expander("🌱 Farm Conditions", expanded=True):
        crop_type = st.selectbox("Primary Crop Type", list(CROP_YIELD_PARAMS.keys()))
        defaults = CROP_DEFAULTS[crop_type]
        land_size = st.slider("Land Size (acres)", 10, 500, 100, 10)
        soil_quality = st.slider("Soil Quality Score", 1.0, 10.0, 6.5, 0.5)
        col1, col2 = st.columns(2)
        with col1: rain_min = st.number_input("Rain Min (mm/year)", value=defaults["rain_min"], step=50)
        with col2: rain_max = st.number_input("Rain Max (mm/year)", value=defaults["rain_max"], step=50)
        col3, col4 = st.columns(2)
        with col3: temp_min = st.number_input("Temp Min (°C)", value=defaults["temp_min"], step=1)
        with col4: temp_max = st.number_input("Temp Max (°C)", value=defaults["temp_max"], step=1)

    with st.expander("💰 Economic Factors", expanded=True):
        col5, col6 = st.columns(2)
        with col5: price_min = st.number_input("Price Min ($)", value=defaults["price_min"], step=1)
        with col6: price_max = st.number_input("Price Max ($)", value=defaults["price_max"], step=1)
        farming_cost = st.number_input("Farming Cost ($/acre)", value=defaults["cost"], step=50)

    with st.expander("🔀 Strategy Options", expanded=True):
        all_crops = list(CROP_YIELD_PARAMS.keys())
        crop_a = st.selectbox("Crop Option A", all_crops)
        crop_b = st.selectbox("Crop Option B", all_crops, index=min(2, len(all_crops)-1))
        irrigation = st.select_slider("Irrigation Level", ["Low","Medium","High"], value="Medium")
        fertilizer = st.select_slider("Fertilizer Level", ["Low","Medium","High"], value="Medium")
        n_simulations = st.select_slider("Simulations", [1000,2000,5000,10000], value=2000)
        risk_tolerance = st.select_slider("Risk Profile", ["Conservative","Balanced","Aggressive"], value="Balanced")
        risk_icons = {"Conservative": "🛡️", "Balanced": "⚖️", "Aggressive": "🚀"}
        st.info(f"{risk_icons[risk_tolerance]} {risk_tolerance} selected")
        run_btn = st.button("🚀 Run Simulation", type="primary", use_container_width=True)

# ── Build strategies & farm/economic objects ───────────────────────────────────
strategies = [
    Strategy(f"{crop_a} · {irrigation} Irrigation · {fertilizer} Fertilizer", crop_a, irrigation, fertilizer),
    Strategy(f"{crop_b} · {irrigation} Irrigation · {fertilizer} Fertilizer", crop_b, irrigation, fertilizer),
    Strategy(f"{crop_a} · High Irrigation · High Fertilizer", crop_a, "High", "High"),
    Strategy(f"{crop_b} · Low Irrigation · Low Fertilizer", crop_b, "Low", "Low"),
]
farm = FarmConditions(crop_type, land_size, soil_quality, float(rain_min), float(rain_max), float(temp_min), float(temp_max))
economics = EconomicFactors(float(price_min), float(price_max), float(farming_cost))

# ── Run simulations ───────────────────────────────────────────────────────────
if run_btn or "results" not in st.session_state:
    with st.spinner("Running Monte Carlo simulations…"):
        results = compare_strategies(farm, economics, strategies, n_simulations)
        st.session_state["results"] = results

results = st.session_state["results"]
best, scores = recommend_strategy(results, risk_tolerance)

# ── KPI Cards ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📊 Simulation Summary</div>', unsafe_allow_html=True)
kpi_cols = st.columns(5)
kpi_data = [
    ("Strategies", len(results)),
    ("Simulations", f"{n_simulations:,}"),
    ("Best Avg Profit", format_currency(max(r.avg_profit for r in results))),
    ("Lowest Risk (Std)", format_currency(min(r.std_dev for r in results))),
    ("Best Prob Profit", format_percent(1 - min(r.prob_of_loss for r in results))),
]
for col, (label, value) in zip(kpi_cols, kpi_data):
    with col:
        st.markdown(f'<div class="metric-card"><div class="value">{value}</div><div class="label">{label}</div></div>', unsafe_allow_html=True)

# ── Recommended Strategy ─────────────────────────────────────────────────────
st.markdown(f"""
<div class="recommend-box" style="color:#7a5200;">
<h3>🏆 Recommended for {risk_tolerance}</h3>
<b>{best.strategy_name}</b><br>
Avg Profit: <b>{format_currency(best.avg_profit)}</b> | Worst Case: <b>{format_currency(best.worst_case)}</b> | Prob Loss: <b>{format_percent(best.prob_of_loss)}</b>
</div>
""", unsafe_allow_html=True)

# ── Strategy Table ───────────────────────────────────────────────────────────
df_table = pd.DataFrame(build_comparison_table(results, risk_tolerance))
def highlight_best(row):
    if row["Strategy"] == best.strategy_name:
        return ["background-color:#fff3cd; font-weight:bold; color:#7a5200"] * len(row)
    return [""] * len(row)

st.dataframe(df_table.style.apply(highlight_best, axis=1), use_container_width=True, hide_index=True)

# ── Visualizations Tabs ──────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📊 Profit & Risk","🎯 Confidence Intervals"])

with tab1:
    st.markdown("**Profit Distribution & Risk Metrics**")
    fig = make_subplots(rows=1, cols=2, subplot_titles=["Profit Histogram","Risk Metrics"], horizontal_spacing=0.12)
    PALETTE = px.colors.qualitative.Bold
    for idx, r in enumerate(results):
        fig.add_trace(go.Histogram(x=r.profits, name=r.strategy_name, opacity=0.7, marker_color=PALETTE[idx%len(PALETTE)]), row=1, col=1)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("**5th–95th Percentile Confidence Intervals**")
    fig2 = go.Figure()
    for idx,r in enumerate(results):
        fig2.add_trace(go.Scatter(x=[r.p5,r.p95], y=[r.strategy_name,r.strategy_name], mode='lines', line=dict(width=14), opacity=0.35, showlegend=False))
        fig2.add_trace(go.Scatter(x=[r.avg_profit], y=[r.strategy_name], mode='markers+text', marker=dict(size=14,symbol='diamond'), text=[format_currency(r.avg_profit)], textposition='middle right'))
    fig2.update_layout(height=400, xaxis_title="Profit ($)")
    st.plotly_chart(fig2, use_container_width=True)

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown('<hr>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center; color:#888; font-size:0.85rem;">🌾 AI Farm Strategy Advisor · Streamlit + NumPy + Plotly</div>', unsafe_allow_html=True)
