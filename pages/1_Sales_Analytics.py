import streamlit as st
import pandas as pd
import plotly.express as px
from components.sidebar import render_sidebar

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Sales Analytics",
    page_icon="📊",
    layout="wide"
)

from auth import require_login
require_login()

render_sidebar()
# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("data/cleaned_retail.csv")

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    return df

df = load_data()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("📊 Sales Analytics")

st.sidebar.markdown("---")

country = st.sidebar.selectbox(

    "🌍 Country",

    ["All"] + sorted(df["Country"].unique())

)

if country != "All":

    df = df[df["Country"] == country]

start = df["InvoiceDate"].min().date()

end = df["InvoiceDate"].max().date()

date = st.sidebar.date_input(

    "📅 Date Range",

    (start, end)

)

if len(date) == 2:

    s, e = date

    df = df[

        (df["InvoiceDate"].dt.date >= s)

        &

        (df["InvoiceDate"].dt.date <= e)

    ]

# --------------------------------------------------
# KPIs
# --------------------------------------------------

revenue = df["TotalPrice"].sum()

orders = df["Invoice"].nunique()

customers = df["Customer ID"].nunique()

products = df["StockCode"].nunique()

# --------------------------------------------------
# HERO
# --------------------------------------------------

st.markdown("""

<div style='
background:linear-gradient(90deg,#2563eb,#1e40af);
padding:28px;
border-radius:22px;
margin-bottom:20px;
'>

<h1 style='color:white;margin:0;'>

📊 Sales Analytics

</h1>

<p style='color:white;font-size:18px;'>

Monitor revenue, products, orders and country-wise sales performance.

</p>

</div>

""",unsafe_allow_html=True)

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

c1,c2,c3,c4=st.columns(4)

with c1:

    st.metric(

        "💰 Revenue",

        f"£{revenue:,.2f}"

    )

with c2:

    st.metric(

        "🛒 Orders",

        f"{orders:,}"

    )

with c3:

    st.metric(

        "👥 Customers",

        f"{customers:,}"

    )

with c4:

    st.metric(

        "📦 Products",

        f"{products:,}"

    )

st.divider()

# --------------------------------------------------
# DAILY SALES
# --------------------------------------------------

daily=(

    df.groupby(

        df["InvoiceDate"].dt.date

    )["TotalPrice"]

    .sum()

    .reset_index()

)

daily.columns=["Date","Revenue"]

fig=px.area(

    daily,

    x="Date",

    y="Revenue",

    title="📈 Daily Revenue Trend",

    color_discrete_sequence=["#2563eb"]

)

fig.update_layout(

    template="plotly_dark",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    height=450

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()
# --------------------------------------------------
# MONTHLY REVENUE
# --------------------------------------------------

monthly = (
    df.groupby(df["InvoiceDate"].dt.to_period("M"))["TotalPrice"]
    .sum()
    .reset_index()
)

monthly["InvoiceDate"] = monthly["InvoiceDate"].astype(str)

# --------------------------------------------------
# TOP PRODUCTS
# --------------------------------------------------

top_products = (
    df.groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# --------------------------------------------------
# TOP COUNTRIES
# --------------------------------------------------

top_countries = (
    df.groupby("Country")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# --------------------------------------------------
# ROW 2
# --------------------------------------------------

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

        height=420,

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

        height=420,

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        coloraxis_showscale=False

    )

    st.plotly_chart(

        fig3,

        use_container_width=True

    )

st.divider()

# --------------------------------------------------
# ROW 3
# --------------------------------------------------

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

        height=520,

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

    fig5 = px.pie(

        top_countries,

        names="Country",

        values="TotalPrice",

        hole=.60,

        title="🌎 Revenue Distribution"

    )

    fig5.update_layout(

        template="plotly_dark",

        height=520,

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)"

    )

    st.plotly_chart(

        fig5,

        use_container_width=True

    )

st.divider()

# --------------------------------------------------
# QUICK ANALYTICS
# --------------------------------------------------

avg_order = revenue/orders

avg_customer = revenue/customers

a1,a2 = st.columns(2)

with a1:

    st.info(f"""

### 📊 Performance Summary

💰 Revenue

**£{revenue:,.2f}**

🛒 Orders

**{orders:,}**

👥 Customers

**{customers:,}**

📦 Products

**{products:,}**

""")

with a2:

    st.success(f"""

### 📈 Key Metrics

💳 Avg Order Value

**£{avg_order:,.2f}**

👤 Avg Customer Value

**£{avg_customer:,.2f}**

🌍 Best Market

**{top_countries.iloc[0]['Country']}**

🔥 Best Product

**{top_products.iloc[0]['Description']}**

""")

st.divider()

# --------------------------------------------------
# AI INSIGHTS
# --------------------------------------------------

st.markdown("## 🤖 AI Business Insights")

st.warning("""

### Recommendations

✅ Increase inventory for the highest-selling products.

✅ Focus marketing campaigns in the highest revenue country.

✅ Reward repeat customers with loyalty programs.

✅ Monitor seasonal monthly revenue trends.

✅ Use customer segmentation to improve retention.

""")

st.divider()

# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------

st.markdown("## 🗂 Dataset Preview")

preview = df.copy()

preview["InvoiceDate"] = preview["InvoiceDate"].dt.strftime("%d-%m-%Y")

st.dataframe(

    preview.head(15),

    use_container_width=True,

    hide_index=True

)

st.divider()

# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(

    "⬇ Download Sales Report",

    csv,

    "sales_report.csv",

    "text/csv"

)

st.divider()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""

<div class='footer'>

<h3 style="color:white;">

📊 RetailPulse AI

</h3>

AI-Powered Retail Intelligence Platform

<br><br>

Developed by <b>Apeksha Kaushik</b>

</div>

""",unsafe_allow_html=True)