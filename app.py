import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from components.sidebar import render_sidebar

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------

st.set_page_config(
    page_title="RetailPulse AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
render_sidebar()
# -----------------------------------------------------
# LOAD CSS
# -----------------------------------------------------

css_file = Path("assets/style.css")

if css_file.exists():

    with open(css_file) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# -----------------------------------------------------
# LOAD DATA
# -----------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("data/cleaned_retail.csv")

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    return df

df = load_data()

# -----------------------------------------------------
# KPIs
# -----------------------------------------------------

revenue = df["TotalPrice"].sum()

customers = df["Customer ID"].nunique()

orders = df["Invoice"].nunique()

products = df["StockCode"].nunique()

# -----------------------------------------------------
# HERO SECTION
# -----------------------------------------------------

st.markdown("""

<div style="background:linear-gradient(90deg,#2563eb,#1d4ed8);
padding:30px;
border-radius:20px;
margin-bottom:20px;">

<h1 style="color:white;margin:0;">
📊 RetailPulse AI
</h1>

<h4 style="color:white;margin-top:10px;">
AI-Powered Retail Intelligence Platform
</h4>

<p style="color:white;font-size:18px;">
Transform Retail Data into Actionable Business Insights
</p>

</div>

""",unsafe_allow_html=True)

# -----------------------------------------------------
# KPI CARDS
# -----------------------------------------------------

c1,c2,c3,c4=st.columns(4)

with c1:

    st.metric(
        "💰 Revenue",
        f"£{revenue:,.2f}"
    )

with c2:

    st.metric(
        "👥 Customers",
        f"{customers:,}"
    )

with c3:

    st.metric(
        "📦 Products",
        f"{products:,}"
    )

with c4:

    st.metric(
        "🛒 Orders",
        f"{orders:,}"
    )

st.divider()

# -----------------------------------------------------
# QUICK SUMMARY
# -----------------------------------------------------

left,right=st.columns([2,1])

with left:

    daily_sales=(

        df.groupby(

            df["InvoiceDate"].dt.date

        )["TotalPrice"]

        .sum()

        .reset_index()

    )

    daily_sales.columns=[

        "Date",

        "Revenue"

    ]

    fig=px.area(

        daily_sales,

        x="Date",

        y="Revenue",

        title="📈 Daily Revenue Trend",

        color_discrete_sequence=["#3B82F6"]

    )

    fig.update_layout(

        template="plotly_dark",

        height=420,

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with right:

    st.markdown("## 🤖 Executive Summary")

    st.success(f"""

### Business Snapshot

💰 Revenue

**£{revenue:,.2f}**

👥 Customers

**{customers:,}**

📦 Products

**{products:,}**

🛒 Orders

**{orders:,}**

""")

st.divider()
# -----------------------------------------------------
# MONTHLY REVENUE
# -----------------------------------------------------

monthly = (
    df.groupby(df["InvoiceDate"].dt.to_period("M"))["TotalPrice"]
    .sum()
    .reset_index()
)

monthly["InvoiceDate"] = monthly["InvoiceDate"].astype(str)

# -----------------------------------------------------
# TOP PRODUCTS
# -----------------------------------------------------

top_products = (
    df.groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# -----------------------------------------------------
# TOP COUNTRIES
# -----------------------------------------------------

top_countries = (
    df.groupby("Country")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# -----------------------------------------------------
# DASHBOARD ROW 2
# -----------------------------------------------------

left,right = st.columns(2)

with left:

    fig2 = px.bar(

        monthly,

        x="InvoiceDate",

        y="TotalPrice",

        title="📅 Monthly Revenue",

        color="TotalPrice",

        color_continuous_scale="Blues"

    )

    fig2.update_layout(

        template="plotly_dark",

        height=430,

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        coloraxis_showscale=False

    )

    st.plotly_chart(

        fig2,

        use_container_width=True

    )

with right:

    fig3 = px.bar(

        top_countries,

        x="Country",

        y="TotalPrice",

        title="🌍 Top Countries",

        color="TotalPrice",

        color_continuous_scale="Viridis"

    )

    fig3.update_layout(

        template="plotly_dark",

        height=430,

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        coloraxis_showscale=False

    )

    st.plotly_chart(

        fig3,

        use_container_width=True

    )

st.divider()

# -----------------------------------------------------
# DASHBOARD ROW 3
# -----------------------------------------------------

left,right = st.columns(2)

with left:

    fig4 = px.bar(

        top_products,

        x="Quantity",

        y="Description",

        orientation="h",

        title="🔥 Top Selling Products",

        color="Quantity",

        color_continuous_scale="Turbo"

    )

    fig4.update_layout(

        template="plotly_dark",

        height=500,

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        coloraxis_showscale=False,

        yaxis_title=""

    )

    st.plotly_chart(

        fig4,

        use_container_width=True

    )

with right:

    st.markdown("## 🧠 AI Business Insights")

    highest_country = top_countries.iloc[0]["Country"]

    highest_product = top_products.iloc[0]["Description"]

    st.info(f"""

### 📈 Revenue Insights

🌍 Highest Revenue Market

**{highest_country}**

🔥 Best Selling Product

**{highest_product}**

💰 Total Revenue

**£{revenue:,.2f}**

👥 Active Customers

**{customers:,}**

📦 Products Sold

**{products:,}**

🛒 Orders Processed

**{orders:,}**

""")

    st.success("""

### 🚀 Recommendations

✅ Focus marketing on the highest revenue country.

✅ Maintain higher inventory for top-selling products.

✅ Reward loyal customers with exclusive offers.

✅ Monitor monthly sales trends for seasonal demand.

""")

st.divider()
# -----------------------------------------------------
# QUICK ANALYTICS
# -----------------------------------------------------

st.markdown("## 📌 Quick Analytics")

a1,a2,a3 = st.columns(3)

with a1:

    avg_order_value = revenue / orders

    st.metric(

        "💳 Average Order Value",

        f"£{avg_order_value:,.2f}"

    )

with a2:

    avg_customer_value = revenue / customers

    st.metric(

        "👤 Customer Lifetime Value",

        f"£{avg_customer_value:,.2f}"

    )

with a3:

    avg_product_sales = revenue / products

    st.metric(

        "📦 Revenue / Product",

        f"£{avg_product_sales:,.2f}"

    )

st.divider()

# -----------------------------------------------------
# COUNTRY REVENUE SHARE
# -----------------------------------------------------

st.markdown("## 🌍 Revenue Distribution")

country_share = (

    df.groupby("Country")["TotalPrice"]

    .sum()

    .reset_index()

)

fig5 = px.pie(

    country_share,

    names="Country",

    values="TotalPrice",

    hole=0.55,

    color_discrete_sequence=px.colors.qualitative.Bold

)

fig5.update_layout(

    template="plotly_dark",

    height=600,

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)"

)

st.plotly_chart(

    fig5,

    use_container_width=True

)

st.divider()

# -----------------------------------------------------
# DATASET PREVIEW
# -----------------------------------------------------

st.markdown("## 🗂 Retail Dataset Preview")

preview = df.copy()

preview["InvoiceDate"] = preview["InvoiceDate"].dt.strftime("%d-%m-%Y")

st.dataframe(

    preview.head(20),

    use_container_width=True,

    hide_index=True

)

st.divider()

# -----------------------------------------------------
# DOWNLOAD REPORT
# -----------------------------------------------------

st.markdown("## 📥 Export Report")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(

    label="⬇ Download Cleaned Dataset",

    data=csv,

    file_name="RetailPulse_Data.csv",

    mime="text/csv"

)

st.divider()

# -----------------------------------------------------
# TECHNOLOGY STACK
# -----------------------------------------------------

left,right = st.columns(2)

with left:

    st.markdown("## ⚙️ Technologies")

    st.success("""

🐍 Python

🐼 Pandas

📊 Plotly

🤖 Scikit-Learn

📈 Prophet

🌐 Streamlit

""")

with right:

    st.markdown("## 📂 Project Modules")

    st.info("""

🏠 Dashboard

📊 Sales Analytics

👥 Customer Analytics

📈 Demand Forecasting

⚠️ Churn Prediction

📦 Inventory Optimization

ℹ️ About

""")

st.divider()
# -----------------------------------------------------
# EXECUTIVE DASHBOARD
# -----------------------------------------------------

st.markdown("## 📈 Executive Dashboard")

highest_country = (
    df.groupby("Country")["TotalPrice"]
    .sum()
    .idxmax()
)

highest_product = (
    df.groupby("Description")["Quantity"]
    .sum()
    .idxmax()
)

highest_sales_day = (
    daily_sales.sort_values(
        "Revenue",
        ascending=False
    )
    .iloc[0]
)

executive = pd.DataFrame({

    "Metric":[

        "Highest Revenue Country",

        "Best Selling Product",

        "Highest Sales Day",

        "Average Order Value",

        "Average Customer Value"

    ],

    "Value":[

        highest_country,

        highest_product,

        str(highest_sales_day["Date"]),

        f"£{avg_order_value:,.2f}",

        f"£{avg_customer_value:,.2f}"

    ]

})

st.dataframe(

    executive,

    use_container_width=True,

    hide_index=True

)

st.divider()

# -----------------------------------------------------
# AI SUMMARY
# -----------------------------------------------------

st.markdown("## 🤖 AI Executive Summary")

st.success(f"""

### RetailPulse AI Summary

📊 Total Revenue:
**£{revenue:,.2f}**

👥 Customers:
**{customers:,}**

🛒 Orders:
**{orders:,}**

📦 Products:
**{products:,}**

🌍 Strongest Market:
**{highest_country}**

🔥 Best Selling Product:
**{highest_product}**

📈 Business Health:
**Healthy Growth**

""")

st.info("""

### Recommended Actions

✅ Increase stock for high-demand products.

✅ Focus promotions on high-value customers.

✅ Continue customer retention campaigns.

✅ Monitor monthly revenue for seasonal changes.

✅ Review inventory weekly using forecast reports.

""")

st.divider()

# -----------------------------------------------------
# PROJECT INFORMATION
# -----------------------------------------------------

st.markdown("## ℹ️ About RetailPulse AI")

st.write("""

RetailPulse AI is an AI-powered Retail Intelligence Platform
developed to help businesses analyze sales,
understand customer behavior,
forecast demand,
predict churn,
and optimize inventory.

The application combines Business Intelligence,
Machine Learning,
Data Analytics,
and Interactive Dashboards
into one unified platform.

""")

st.divider()

# -----------------------------------------------------
# DEVELOPER
# -----------------------------------------------------

st.markdown("## 👩‍💻 Developer")

col1, col2 = st.columns([1,3])

with col1:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        width=120
    )

with col2:

    st.markdown("""

### Apeksha Kaushik

**B.Tech Computer Science Engineering**

Aspiring Data Scientist | Machine Learning Enthusiast

#### Skills

- Python
- Machine Learning
- Data Analytics
- SQL
- Streamlit
- Pandas
- Scikit-Learn
- Prophet
- Plotly

""")

st.divider()

# -----------------------------------------------------
# FOOTER
# -----------------------------------------------------

st.markdown("""

---

<div style='text-align:center;
padding:20px;
border-radius:12px;
background:#111827;'>

<h3 style='color:white;'>

📊 RetailPulse AI

</h3>

<p style='color:#9CA3AF;'>

AI-Powered Retail Intelligence Platform

</p>

<p style='color:#9CA3AF;'>

Developed by <b>Apeksha Kaushik</b>

</p>

<p style='color:#9CA3AF;'>

© 2026 All Rights Reserved

</p>

</div>

""", unsafe_allow_html=True)