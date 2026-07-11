import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from components.sidebar import render_sidebar

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RetailPulse AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# AUTHENTICATION GATE (shared across all pages — see auth.py)
# ============================================================

from auth import require_login
require_login()

# ============================================================
# SIDEBAR
# ============================================================

render_sidebar()

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_retail.csv")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    return df

df = load_data()

# ============================================================
# CORE METRICS
# ============================================================

revenue = df["TotalPrice"].sum()
customers = df["Customer ID"].nunique()
orders = df["Invoice"].nunique()
products = df["StockCode"].nunique()

avg_order_value = revenue / orders
avg_customer_value = revenue / customers

daily_sales = (
    df.groupby(df["InvoiceDate"].dt.date)["TotalPrice"]
    .sum()
    .reset_index()
)
daily_sales.columns = ["Date", "Revenue"]

# simple week-over-week trend for KPI badges
if len(daily_sales) >= 14:
    last7 = daily_sales.tail(7)["Revenue"].sum()
    prev7 = daily_sales.tail(14).head(7)["Revenue"].sum()
    revenue_trend = ((last7 - prev7) / prev7 * 100) if prev7 else 0
else:
    revenue_trend = 0

monthly = (
    df.groupby(df["InvoiceDate"].dt.to_period("M"))["TotalPrice"]
    .sum()
    .reset_index()
)
monthly["InvoiceDate"] = monthly["InvoiceDate"].astype(str)

top_products = (
    df.groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

top_countries = (
    df.groupby("Country")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

country_share = df.groupby("Country")["TotalPrice"].sum().reset_index()

highest_country = top_countries.iloc[0]["Country"]
highest_product = top_products.iloc[0]["Description"]

# ============================================================
# SHARED PLOTLY THEME
# ============================================================

FONT = "Inter, -apple-system, Segoe UI, sans-serif"
GRID_COLOR = "rgba(255,255,255,.06)"
TEXT_COLOR = "#94A3B8"


def style_fig(fig, height=400):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT, color=TEXT_COLOR, size=13),
        title=dict(font=dict(size=16, color="#E2E8F0", family=FONT)),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(0,0,0,0)",
            font=dict(color=TEXT_COLOR, size=12),
        ),
        hoverlabel=dict(
            bgcolor="#1E293B",
            font=dict(family=FONT, color="#F1F5F9", size=12),
            bordercolor="rgba(255,255,255,.1)",
        ),
        xaxis=dict(showgrid=False, zeroline=False, linecolor=GRID_COLOR),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, zeroline=False),
    )
    return fig


# ============================================================
# HERO SECTION
# ============================================================

welcome_name = st.session_state.get("user_name", "").split(" ")[0] if st.session_state.get("user_name") else ""
eyebrow_text = f"WELCOME BACK, {welcome_name.upper()}" if welcome_name else "ENTERPRISE RETAIL INTELLIGENCE"

st.markdown(
    f"""
<div class="hero-card">
  <div class="hero-eyebrow">{eyebrow_text}</div>
  <h1 class="hero-title">RetailPulse AI</h1>
  <p class="hero-subtitle">
    Turning raw transaction data into revenue-driving decisions —
    sales analytics, customer intelligence, demand forecasting and
    inventory optimization in a single platform.
  </p>
  <div class="hero-tags">
    <span class="hero-tag">📈 Sales Analytics</span>
    <span class="hero-tag">👥 Customer Intelligence</span>
    <span class="hero-tag">🤖 Machine Learning</span>
    <span class="hero-tag">📦 Inventory Optimization</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# 4 PREMIUM KPI CARDS
# ============================================================

trend_display = f"{'▲' if revenue_trend >= 0 else '▼'} {abs(revenue_trend):.1f}% vs prior week"

kpis = [
    ("💰", "Total Revenue", f"£{revenue:,.0f}", "#22C55E", trend_display),
    ("👥", "Customers", f"{customers:,}", "#3B82F6", "Unique buyers"),
    ("📦", "Products", f"{products:,}", "#F59E0B", "Active SKUs"),
    ("🛒", "Orders", f"{orders:,}", "#A855F7", "Total invoices"),
]

cols = st.columns(4)
for col, (icon, label, value, color, note) in zip(cols, kpis):
    with col:
        st.markdown(
            f"""
<div class="kpi-card" style="--accent:{color};">
  <div class="kpi-icon">{icon}</div>
  <div class="kpi-label">{label}</div>
  <div class="kpi-value">{value}</div>
  <div class="kpi-note" style="color:{color};">{note}</div>
</div>
""",
            unsafe_allow_html=True,
        )

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

# ============================================================
# REVENUE TREND + AI INSIGHTS
# ============================================================

left, right = st.columns([2, 1])

with left:
    fig = px.area(
        daily_sales,
        x="Date",
        y="Revenue",
        title="Daily Revenue Trend",
        color_discrete_sequence=["#22C55E"],
    )
    fig.update_traces(line=dict(width=2.5), fillcolor="rgba(34,197,94,.12)")
    style_fig(fig, height=420)
    st.markdown('<div class="chart-shell">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown(
        f"""
<div class="ai-card">
  <div class="ai-header">
    <span class="ai-badge">AI</span>
    <span class="ai-title">Business Insights</span>
  </div>
  <div class="ai-body">
    <div class="ai-row">
      <span>🌍 Strongest market</span>
      <b>{highest_country}</b>
    </div>
    <div class="ai-row">
      <span>🔥 Best-selling product</span>
      <b title="{highest_product}">{highest_product[:28] + ("…" if len(highest_product) > 28 else "")}</b>
    </div>
    <div class="ai-row">
      <span>💳 Avg. order value</span>
      <b>£{avg_order_value:,.2f}</b>
    </div>
    <div class="ai-row">
      <span>👤 Avg. customer value</span>
      <b>£{avg_customer_value:,.2f}</b>
    </div>
  </div>
  <div class="ai-footer">
    ✔ Revenue trend is {"positive" if revenue_trend >= 0 else "softening"}.<br>
    ✔ Monitor stock for top-selling inventory.<br>
    ✔ Customer activity remains healthy.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

# ============================================================
# MONTHLY REVENUE + TOP COUNTRIES
# ============================================================

left, right = st.columns(2)

with left:
    fig2 = px.bar(
        monthly,
        x="InvoiceDate",
        y="TotalPrice",
        title="Monthly Revenue",
        color="TotalPrice",
        color_continuous_scale=["#1E3A8A", "#3B82F6", "#93C5FD"],
    )
    fig2.update_layout(coloraxis_showscale=False)
    style_fig(fig2, height=400)
    st.markdown('<div class="chart-shell">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    fig3 = px.bar(
        top_countries,
        x="Country",
        y="TotalPrice",
        title="Top Countries by Revenue",
        color="TotalPrice",
        color_continuous_scale=["#78350F", "#F59E0B", "#FCD34D"],
    )
    fig3.update_layout(coloraxis_showscale=False)
    style_fig(fig3, height=400)
    st.markdown('<div class="chart-shell">', unsafe_allow_html=True)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

# ============================================================
# TOP PRODUCTS + REVENUE DISTRIBUTION
# ============================================================

left, right = st.columns(2)

with left:
    fig4 = px.bar(
        top_products,
        x="Quantity",
        y="Description",
        orientation="h",
        title="Top Selling Products",
        color="Quantity",
        color_continuous_scale=["#4C1D95", "#A855F7", "#D8B4FE"],
    )
    fig4.update_layout(coloraxis_showscale=False, yaxis_title="")
    fig4.update_yaxes(autorange="reversed")
    style_fig(fig4, height=460)
    st.markdown('<div class="chart-shell">', unsafe_allow_html=True)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    fig5 = px.pie(
        country_share,
        names="Country",
        values="TotalPrice",
        hole=0.62,
        title="Revenue Distribution by Country",
        color_discrete_sequence=[
            "#22C55E", "#3B82F6", "#F59E0B", "#A855F7",
            "#EC4899", "#14B8A6", "#EAB308", "#6366F1",
        ],
    )
    fig5.update_traces(textinfo="none", hovertemplate="%{label}<br>£%{value:,.0f}<extra></extra>")
    style_fig(fig5, height=460)
    st.markdown('<div class="chart-shell">', unsafe_allow_html=True)
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

# ============================================================
# DOWNLOAD REPORT
# ============================================================

st.markdown('<div class="section-heading">Export</div>', unsafe_allow_html=True)

csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇ Download Cleaned Dataset (CSV)",
    data=csv,
    file_name="RetailPulse_Data.csv",
    mime="text/csv",
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