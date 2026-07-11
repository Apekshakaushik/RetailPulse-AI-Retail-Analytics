import streamlit as st
import pandas as pd
import plotly.express as px
from components.sidebar import render_sidebar
# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Analytics",
    page_icon="👥",
    layout="wide"
)
render_sidebar()
# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    return pd.read_csv("data/customer_segments.csv")

df = load_data()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("👥 Customer Analytics")

segment = st.sidebar.selectbox(

    "Customer Segment",

    ["All"] + sorted(df["Customer_Segment"].unique())

)

if segment != "All":

    df = df[df["Customer_Segment"] == segment]

# --------------------------------------------------
# KPI VALUES
# --------------------------------------------------

customers = len(df)

avg_recency = round(df["Recency"].mean(),2)

avg_frequency = round(df["Frequency"].mean(),2)

avg_monetary = round(df["Monetary"].mean(),2)

vip = len(

    df[df["Monetary"]>=df["Monetary"].quantile(.95)]

)

risk = len(

    df[df["Customer_Segment"]=="At Risk Customers"]

)

# --------------------------------------------------
# HERO
# --------------------------------------------------

st.markdown(
    """
<div style="background:linear-gradient(90deg,#7c3aed,#5b21b6); padding:28px; border-radius:22px; margin-bottom:20px;">

<h1 style="color:white; margin:0;">
👥 Customer Analytics
</h1>

<p style="color:white; font-size:18px;">
Customer Segmentation using RFM Analysis & Machine Learning
</p>

</div>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

c1,c2,c3,c4,c5=st.columns(5)

with c1:

    st.metric(

        "👥 Customers",

        customers

    )

with c2:

    st.metric(

        "👑 VIP",

        vip

    )

with c3:

    st.metric(

        "⚠ At Risk",

        risk

    )

with c4:

    st.metric(

        "🛒 Avg Frequency",

        avg_frequency

    )

with c5:

    st.metric(

        "💰 Avg Spend",

        f"£{avg_monetary:,.2f}"

    )

st.divider()

# --------------------------------------------------
# RFM SCATTER
# --------------------------------------------------

fig = px.scatter(

    df,

    x="Frequency",

    y="Monetary",

    color="Customer_Segment",

    size="Recency",

    hover_data=["Customer ID"],

    title="📈 RFM Customer Segmentation"

)

fig.update_layout(

    template="plotly_dark",

    height=550,

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

# --------------------------------------------------
# SEGMENT DISTRIBUTION
# --------------------------------------------------

left,right=st.columns(2)

with left:

    segment_count=(

        df["Customer_Segment"]

        .value_counts()

        .reset_index()

    )

    segment_count.columns=[

        "Segment",

        "Customers"

    ]

    fig2=px.pie(

        segment_count,

        names="Segment",

        values="Customers",

        hole=.60,

        title="🥧 Customer Distribution"

    )

    fig2.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        height=500

    )

    st.plotly_chart(

        fig2,

        use_container_width=True

    )

with right:

    fig3=px.bar(

        segment_count,

        x="Segment",

        y="Customers",

        color="Customers",

        title="📊 Customer Segments",

        color_continuous_scale="Purples"

    )

    fig3.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        coloraxis_showscale=False,

        height=500

    )

    st.plotly_chart(

        fig3,

        use_container_width=True

    )

st.divider()
# --------------------------------------------------
# TOP 20 CUSTOMERS
# --------------------------------------------------

st.markdown("## 👑 Top 20 High Value Customers")

top_customers = (

    df.sort_values(

        "Monetary",

        ascending=False

    )

    .head(20)

)

st.dataframe(

    top_customers,

    use_container_width=True,

    hide_index=True

)

st.divider()

# --------------------------------------------------
# CUSTOMER SEARCH
# --------------------------------------------------

st.markdown("## 🔍 Search Customer")

customer = st.text_input(

    "Enter Customer ID"

)

if customer:

    result = df[

        df["Customer ID"].astype(str)

        ==

        customer

    ]

    if len(result):

        st.success("✅ Customer Found")

        st.dataframe(

            result,

            use_container_width=True,

            hide_index=True

        )

    else:

        st.error("❌ Customer Not Found")

st.divider()

# --------------------------------------------------
# MONETARY DISTRIBUTION
# --------------------------------------------------

fig4 = px.histogram(

    df,

    x="Monetary",

    nbins=30,

    color_discrete_sequence=["#7C3AED"],

    title="💰 Customer Spending Distribution"

)

fig4.update_layout(

    template="plotly_dark",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    height=450

)

st.plotly_chart(

    fig4,

    use_container_width=True

)

st.divider()

# --------------------------------------------------
# VIP & RISK TABLES
# --------------------------------------------------

left,right = st.columns(2)

with left:

    st.markdown("### 👑 VIP Customers")

    vip_df = (

        df

        .sort_values(

            "Monetary",

            ascending=False

        )

        .head(10)

    )

    st.dataframe(

        vip_df,

        use_container_width=True,

        hide_index=True

    )

with right:

    st.markdown("### ⚠️ At Risk Customers")

    risk_df = df[

        df["Customer_Segment"]

        ==

        "At Risk Customers"

    ]

    st.dataframe(

        risk_df.head(10),

        use_container_width=True,

        hide_index=True

    )

st.divider()

# --------------------------------------------------
# QUICK ANALYTICS
# --------------------------------------------------

left,right = st.columns(2)

with left:

    st.success(f"""

### 📈 Customer Summary

👥 Total Customers

**{customers:,}**

👑 VIP Customers

**{vip:,}**

⚠️ At Risk Customers

**{risk:,}**

""")

with right:

    st.info(f"""

### 💰 RFM Summary

📅 Avg Recency

**{avg_recency}**

🛒 Avg Frequency

**{avg_frequency}**

💷 Avg Monetary

**£{avg_monetary:,.2f}**

""")

st.divider()

# --------------------------------------------------
# AI INSIGHTS
# --------------------------------------------------

st.markdown("## 🤖 AI Customer Insights")

st.warning("""

### Recommendations

✅ Reward VIP customers with exclusive loyalty benefits.

✅ Re-engage At Risk customers through discounts and email campaigns.

✅ Target Regular Customers with personalized offers.

✅ Monitor customer purchase frequency every month.

✅ Build customer retention strategies using RFM scores.

""")

st.divider()

# --------------------------------------------------
# DOWNLOAD REPORT
# --------------------------------------------------

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(

    "⬇ Download Customer Report",

    csv,

    "customer_report.csv",

    "text/csv"

)

st.divider()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""

<div class='footer'>

<h3 style='color:white;'>

👥 Customer Analytics

</h3>

RetailPulse AI

<br><br>

Developed by <b>Apeksha Kaushik</b>

</div>

""",unsafe_allow_html=True)