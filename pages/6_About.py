import streamlit as st
from components.sidebar import render_sidebar
from pathlib import Path

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)

render_sidebar()

# --------------------------------------------------
# HERO
# --------------------------------------------------

st.markdown("""
<div style="background:linear-gradient(90deg,#2563eb,#7c3aed);
padding:30px;
border-radius:20px;
margin-bottom:25px;">

<h1 style="color:white;margin-bottom:10px;">
ℹ️ About RetailPulse AI
</h1>

<p style="color:white;font-size:18px;">
AI-Powered Retail Intelligence Platform built using Machine Learning, Business Intelligence and Interactive Analytics.
</p>

</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# PROFILE
# --------------------------------------------------

col1, col2 = st.columns([1, 2])

with col1:
    BASE_DIR = Path(__file__).resolve().parent.parent

PROFILE = BASE_DIR / "assets" / "profile.jpg"

st.image("profile.jpg", width=260)

with col2:

    st.markdown("# 👩‍💻 Apeksha Kaushik")

    st.markdown("""
### Data Scientist | Machine Learning Enthusiast

🎓 **B.Tech Computer Science Engineering**

📍 **India**

I enjoy building data-driven applications that solve real-world business problems using Machine Learning, Data Analytics and Business Intelligence.

RetailPulse AI combines analytics and predictive models into one platform that helps businesses understand sales performance, customer behaviour, demand trends and inventory planning.
""")

st.divider()

# --------------------------------------------------
# PROJECT OVERVIEW
# --------------------------------------------------

st.header("📊 Project Overview")

st.info("""
RetailPulse AI is an AI-powered Retail Analytics Platform developed using Python and Streamlit.

The application enables businesses to:

• Analyze retail sales performance

• Understand customer purchasing behaviour

• Forecast future demand

• Predict customer churn

• Optimize inventory

• Generate interactive business insights
""")

st.divider()

# --------------------------------------------------
# FEATURES
# --------------------------------------------------

st.header("🚀 Key Features")

c1, c2 = st.columns(2)

with c1:

    st.success("""
### 📊 Analytics

✔ Sales Dashboard

✔ Customer Analytics

✔ Revenue Analysis

✔ Product Insights

✔ Country-wise Performance

✔ Interactive Visualizations
""")

with c2:

    st.success("""
### 🤖 AI Modules

✔ Customer Segmentation

✔ Demand Forecasting

✔ Churn Prediction

✔ Inventory Optimization

✔ Download Reports

✔ Business Recommendations
""")

st.divider()

# --------------------------------------------------
# TECH STACK
# --------------------------------------------------

st.header("🛠 Technology Stack")

t1, t2, t3 = st.columns(3)

with t1:

    st.markdown("""
### Programming

- Python
- SQL
- Pandas
- NumPy
""")

with t2:

    st.markdown("""
### Machine Learning

- Scikit-Learn
- Prophet
- K-Means Clustering
- Random Forest
""")

with t3:

    st.markdown("""
### Dashboard

- Streamlit
- Plotly
- Matplotlib
- GitHub
""")

st.divider()

# --------------------------------------------------
# MODELS
# --------------------------------------------------

st.header("🤖 Machine Learning Models")

m1, m2, m3, m4 = st.columns(4)

m1.metric("Customer Segmentation", "K-Means")
m2.metric("Demand Forecasting", "Prophet")
m3.metric("Churn Prediction", "Random Forest")
m4.metric("Dashboard", "Streamlit")

st.divider()

# --------------------------------------------------
# WORKFLOW
# --------------------------------------------------

st.header("🔄 Project Workflow")

st.code("""
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
""")

st.divider()

# --------------------------------------------------
# PROJECT STATISTICS
# --------------------------------------------------

st.header("📈 Project Highlights")

a, b, c, d = st.columns(4)

a.metric("Modules", "6")
b.metric("ML Models", "3")
c.metric("Charts", "20+")
d.metric("Reports", "5")

st.divider()

# --------------------------------------------------
# CONTACT
# --------------------------------------------------

st.header("📬 Connect With Me")

st.markdown("""
**👩‍💻 Apeksha Kaushik**

🔗 **LinkedIn**

https://www.linkedin.com/in/apeksha-kaushik-378000253

💻 **GitHub**

https://github.com/Apekshakaushik

📧 **Email**

apekshakaushik16@gmail.com
""")

st.divider()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div style="text-align:center;padding:25px;">

<h2 style="color:white;">
📊 RetailPulse AI
</h2>

<p style="color:#B8C0CC;">
AI-Powered Retail Intelligence Platform
</p>

<p style="color:#B8C0CC;">
Developed by <b>Apeksha Kaushik</b>
</p>

<p style="color:#B8C0CC;">
© 2026 All Rights Reserved
</p>

</div>
""", unsafe_allow_html=True)