import streamlit as st

def render_sidebar():

    st.sidebar.markdown("""

<div style="text-align:center;padding:10px 0;">

<h1 style="color:#3B82F6;margin-bottom:0;">
📊
</h1>

<h2 style="color:white;margin-top:5px;">
RetailPulse AI
</h2>

<p style="color:#9CA3AF;font-size:14px;">
AI-Powered Retail Intelligence
</p>

</div>

<hr style="border:1px solid rgba(255,255,255,.08);">

""", unsafe_allow_html=True)

    st.sidebar.markdown("### 📌 Dashboard")

    st.sidebar.info("""

🏠 Home

📊 Sales Analytics

👥 Customer Analytics

📈 Demand Forecasting

⚠️ Churn Prediction

📦 Inventory Optimization

ℹ️ About

""")

    st.sidebar.markdown("---")

    st.sidebar.markdown("### 🚀 Features")

    st.sidebar.success("""

✔ Machine Learning

✔ RFM Analysis

✔ Prophet Forecasting

✔ Random Forest

✔ Interactive Dashboard

✔ Inventory Planning

""")

    st.sidebar.markdown("---")

    st.sidebar.markdown("### 🛠 Tech Stack")

    st.sidebar.markdown("""

- Python

- Streamlit

- Plotly

- Pandas

- Scikit-Learn

- Prophet

""")

    st.sidebar.markdown("---")

    st.sidebar.markdown("""

<div style="text-align:center;">

<h4 style="color:white;">
👩‍💻 Developer
</h4>

<b style="color:#3B82F6;">
Apeksha Kaushik
</b>

<br><br>

<span style="color:#9CA3AF;">
RetailPulse AI v4
</span>

</div>

""", unsafe_allow_html=True)