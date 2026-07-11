import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from components.sidebar import render_sidebar

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Demand Forecasting",
    page_icon="📈",
    layout="wide"
)

render_sidebar()

from auth import require_login
require_login()
# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("data/sales_forecast.csv")

    df["ds"] = pd.to_datetime(df["ds"])

    return df

forecast = load_data()

# --------------------------------------------------
# KPI VALUES
# --------------------------------------------------

forecast_days = len(forecast)

avg_sales = forecast["yhat"].mean()

highest_sales = forecast["yhat"].max()

lowest_sales = forecast["yhat"].min()

expected_revenue = forecast["yhat"].sum()

# --------------------------------------------------
# HERO
# --------------------------------------------------

st.markdown("""

<div style='
background:linear-gradient(90deg,#ea580c,#c2410c);
padding:28px;
border-radius:22px;
margin-bottom:20px;
'>

<h1 style='color:white;margin:0;'>

📈 Demand Forecasting

</h1>

<p style='color:white;font-size:18px;'>

Sales Prediction using Facebook Prophet

</p>

</div>

""",unsafe_allow_html=True)

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

c1,c2,c3,c4,c5=st.columns(5)

with c1:

    st.metric(

        "📅 Days",

        forecast_days

    )

with c2:

    st.metric(

        "💰 Avg Forecast",

        f"£{avg_sales:,.0f}"

    )

with c3:

    st.metric(

        "📈 Highest",

        f"£{highest_sales:,.0f}"

    )

with c4:

    st.metric(

        "📉 Lowest",

        f"£{lowest_sales:,.0f}"

    )

with c5:

    st.metric(

        "💷 Total Forecast",

        f"£{expected_revenue:,.0f}"

    )

st.divider()

# --------------------------------------------------
# FORECAST CHART
# --------------------------------------------------

fig = go.Figure()

fig.add_trace(

    go.Scatter(

        x=forecast["ds"],

        y=forecast["yhat"],

        mode="lines",

        line=dict(

            color="#F97316",

            width=4

        ),

        name="Forecast"

    )

)

fig.add_trace(

    go.Scatter(

        x=forecast["ds"],

        y=forecast["yhat_upper"],

        line=dict(width=0),

        showlegend=False

    )

)

fig.add_trace(

    go.Scatter(

        x=forecast["ds"],

        y=forecast["yhat_lower"],

        fill="tonexty",

        line=dict(width=0),

        fillcolor="rgba(249,115,22,.20)",

        name="Confidence Interval"

    )

)

fig.update_layout(

    template="plotly_dark",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    height=600,

    title="📈 Sales Forecast"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

# --------------------------------------------------
# MONTHLY FORECAST
# --------------------------------------------------

forecast["Month"] = forecast["ds"].dt.strftime("%Y-%m")

monthly = (

    forecast

    .groupby("Month")["yhat"]

    .sum()

    .reset_index()

)

fig2 = px.bar(

    monthly,

    x="Month",

    y="yhat",

    title="📅 Monthly Forecast Revenue",

    color="yhat",

    color_continuous_scale="Oranges"

)

fig2.update_layout(

    template="plotly_dark",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    coloraxis_showscale=False,

    height=450

)

st.plotly_chart(

    fig2,

    use_container_width=True

)

st.divider()

# --------------------------------------------------
# FORECAST TABLE
# --------------------------------------------------

st.markdown("## 📋 Forecast Data")

table = forecast[

    [

        "ds",

        "yhat",

        "yhat_lower",

        "yhat_upper"

    ]

].copy()

table.columns = [

    "Date",

    "Forecast",

    "Lower",

    "Upper"

]

table["Forecast"] = table["Forecast"].round(2)

table["Lower"] = table["Lower"].round(2)

table["Upper"] = table["Upper"].round(2)

st.dataframe(

    table,

    use_container_width=True,

    hide_index=True

)

st.divider()

# --------------------------------------------------
# FORECAST SUMMARY
# --------------------------------------------------

next30 = forecast.tail(30)

predicted = next30["yhat"].sum()

avg_day = next30["yhat"].mean()

highest = next30["yhat"].max()

lowest = next30["yhat"].min()

left,right = st.columns(2)

with left:

    st.success(f"""

### 📈 Forecast Summary

💰 Expected Revenue

**£{predicted:,.2f}**

📅 Average Daily Forecast

**£{avg_day:,.2f}**

""")

with right:

    st.info(f"""

### 📊 Forecast Range

📈 Highest

**£{highest:,.2f}**

📉 Lowest

**£{lowest:,.2f}**

""")

st.divider()

# --------------------------------------------------
# FORECAST DISTRIBUTION
# --------------------------------------------------

fig3 = px.histogram(

    forecast,

    x="yhat",

    nbins=30,

    title="📊 Forecast Distribution",

    color_discrete_sequence=["#F97316"]

)

fig3.update_layout(

    template="plotly_dark",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    height=450

)

st.plotly_chart(

    fig3,

    use_container_width=True

)

st.divider()

# --------------------------------------------------
# AI INSIGHTS
# --------------------------------------------------

trend = "📈 Increasing"

if next30["yhat"].iloc[-1] < next30["yhat"].iloc[0]:

    trend = "📉 Decreasing"

st.markdown("## 🤖 AI Forecast Insights")

st.warning(f"""

### Business Recommendations

**Trend:** {trend}

✅ Prepare inventory based on predicted demand.

✅ Increase stock before forecasted peak sales.

✅ Schedule marketing campaigns during high-demand periods.

✅ Review forecast weekly for better planning.

""")

st.divider()

# --------------------------------------------------
# DOWNLOAD REPORT
# --------------------------------------------------

csv = table.to_csv(index=False).encode("utf-8")

st.download_button(

    "⬇ Download Forecast Report",

    csv,

    "forecast_report.csv",

    "text/csv"

)

st.divider()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""

<div class='footer'>

<h3 style='color:white;'>

📈 Demand Forecasting

</h3>

RetailPulse AI

<br><br>

Developed by <b>Apeksha Kaushik</b>

</div>

""", unsafe_allow_html=True)