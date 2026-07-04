import streamlit as st
import pandas as pd

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="RetailPulse AI",
    page_icon="📊",
    layout="wide"
)

# ---------------------------
# Load Dataset
# ---------------------------
df = pd.read_csv("../data/cleaned_retail.csv")

# ---------------------------
# Calculate KPIs
# ---------------------------
total_revenue = df["TotalPrice"].sum()
total_customers = df["Customer ID"].nunique()
total_products = df["StockCode"].nunique()
total_orders = df["Invoice"].nunique()

# ---------------------------
# Dashboard Title
# ---------------------------
st.title("📊 RetailPulse AI Retail Analytics Dashboard")

st.markdown("""
Welcome to the **AI-Powered Retail Analytics Dashboard**.

This dashboard provides business insights using Machine Learning and Data Analytics.
""")

st.divider()

# ---------------------------
# KPI Cards
# ---------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Total Revenue", f"£{total_revenue:,.2f}")

with col2:
    st.metric("👥 Customers", total_customers)

with col3:
    st.metric("📦 Products", total_products)

with col4:
    st.metric("🛒 Orders", total_orders)