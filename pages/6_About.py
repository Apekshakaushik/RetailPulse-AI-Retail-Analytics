import streamlit as st
from pathlib import Path
from components.sidebar import render_sidebar

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide",
)

from auth import require_login
require_login()

render_sidebar()

# ============================================================
# BRAND BADGE + HERO
# ============================================================

st.markdown(
    """
<div class="brand-badge">RETAILPULSE AI</div>
<div class="brand-tagline">ENTERPRISE RETAIL ANALYTICS</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero-card">
  <div class="hero-eyebrow">ABOUT THE PLATFORM</div>
  <h1 class="hero-title">RetailPulse AI</h1>
  <p class="hero-subtitle">
    An AI-powered retail intelligence platform combining machine learning,
    business analytics, and interactive dashboards into one enterprise product.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# DEVELOPER CREDIT — minimal, no fluff
# ============================================================

st.markdown(
    """
<div class="dev-credit">
  <div class="dev-avatar">AK</div>
  <div class="dev-name">Developed by Apeksha Kaushik</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

# ============================================================
# PROJECT OVERVIEW
# ============================================================

st.markdown('<div class="section-heading">Project Overview</div>', unsafe_allow_html=True)

st.markdown(
    """
<div class="chart-shell" style="padding:22px;">
  <p style="color:#CBD5E1;font-size:14.5px;line-height:1.9;margin:0;">
    RetailPulse AI is an AI-powered retail analytics platform built with Python and Streamlit.
    It enables businesses to analyze sales performance, understand customer purchasing behaviour,
    forecast future demand, predict customer churn, optimize inventory, and generate interactive
    business insights — all from a single platform.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

# ============================================================
# KEY FEATURES
# ============================================================

st.markdown('<div class="section-heading">Key Features</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    st.markdown(
        """
<div class="ai-card">
  <div class="ai-header">
    <span class="ai-badge">📊</span>
    <span class="ai-title">Analytics</span>
  </div>
  <div class="ai-footer">
    ✔ Sales dashboard<br>
    ✔ Customer analytics<br>
    ✔ Revenue analysis<br>
    ✔ Product insights<br>
    ✔ Country-wise performance<br>
    ✔ Interactive visualizations
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
<div class="ai-card">
  <div class="ai-header">
    <span class="ai-badge">🤖</span>
    <span class="ai-title">AI Modules</span>
  </div>
  <div class="ai-footer">
    ✔ Customer segmentation<br>
    ✔ Demand forecasting<br>
    ✔ Churn prediction<br>
    ✔ Inventory optimization<br>
    ✔ Downloadable reports<br>
    ✔ Business recommendations
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

# ============================================================
# TECHNOLOGY STACK
# ============================================================

st.markdown('<div class="section-heading">Technology Stack</div>', unsafe_allow_html=True)

t1, t2, t3 = st.columns(3)
stack = [
    ("Programming", ["Python", "SQL", "Pandas", "NumPy"], "#3B82F6"),
    ("Machine Learning", ["Scikit-Learn", "Prophet", "K-Means", "Random Forest"], "#A855F7"),
    ("Dashboard", ["Streamlit", "Plotly", "Matplotlib", "GitHub"], "#22C55E"),
]

for col, (title, items, color) in zip([t1, t2, t3], stack):
    with col:
        rows = "".join(f"<div class='ai-row'><span>• {i}</span></div>" for i in items)
        st.markdown(
            f"""
<div class="kpi-card" style="--accent:{color};min-height:auto;">
  <div class="kpi-label">{title}</div>
  <div style="margin-top:12px;">{rows}</div>
</div>
""",
            unsafe_allow_html=True,
        )

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

# ============================================================
# MODELS + PROJECT HIGHLIGHTS
# ============================================================

st.markdown('<div class="section-heading">Machine Learning Models</div>', unsafe_allow_html=True)

m_cols = st.columns(4)
model_stats = [
    ("Customer Segmentation", "K-Means", "#3B82F6"),
    ("Demand Forecasting", "Prophet", "#22C55E"),
    ("Churn Prediction", "Random Forest", "#F59E0B"),
    ("Dashboard Engine", "Streamlit", "#A855F7"),
]
for col, (label, value, color) in zip(m_cols, model_stats):
    with col:
        st.markdown(
            f"""
<div class="kpi-card" style="--accent:{color};min-height:110px;">
  <div class="kpi-label">{label}</div>
  <div class="kpi-value" style="font-size:22px;">{value}</div>
</div>
""",
            unsafe_allow_html=True,
        )

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

h_cols = st.columns(4)
highlight_stats = [
    ("Modules", "6", "#3B82F6"),
    ("ML Models", "3", "#22C55E"),
    ("Charts", "20+", "#F59E0B"),
    ("Reports", "5", "#A855F7"),
]
for col, (label, value, color) in zip(h_cols, highlight_stats):
    with col:
        st.markdown(
            f"""
<div class="kpi-card" style="--accent:{color};min-height:110px;">
  <div class="kpi-label">{label}</div>
  <div class="kpi-value" style="font-size:26px;">{value}</div>
</div>
""",
            unsafe_allow_html=True,
        )

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

# ============================================================
# WORKFLOW
# ============================================================

st.markdown('<div class="section-heading">Project Workflow</div>', unsafe_allow_html=True)

st.markdown(
    """
<div class="chart-shell" style="padding:20px;">
<pre style="color:#94A3B8;font-size:13px;line-height:1.7;margin:0;font-family:'Inter',monospace;">
Retail Dataset
      │
      ▼
Data Cleaning
      │
      ▼
Feature Engineering
      │
      ▼
Machine Learning
 ├── K-Means
 ├── Prophet
 └── Random Forest
      │
      ▼
Interactive Dashboard
      │
      ▼
Business Insights
</pre>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

# ============================================================
# CONTACT
# ============================================================

st.markdown('<div class="section-heading">Connect</div>', unsafe_allow_html=True)

st.markdown(
    """
<div class="ai-card">
  <div class="ai-row"><span>🔗 LinkedIn</span><b>apeksha-kaushik-378000253</b></div>
  <div class="ai-row"><span>💻 GitHub</span><b>Apekshakaushik</b></div>
  <div class="ai-row"><span>📧 Email</span><b>apekshakaushik16@gmail.com</b></div>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="app-footer">
  <div class="footer-title">📊 RetailPulse AI</div>
  <div class="footer-sub">AI-Powered Retail Intelligence Platform</div>
  <div class="footer-meta">Developed by Apeksha Kaushik · © 2026 All Rights Reserved</div>
</div>
""",
    unsafe_allow_html=True,
)