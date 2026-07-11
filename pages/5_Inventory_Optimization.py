import streamlit as st
import pandas as pd
import plotly.express as px
from components.sidebar import render_sidebar

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Inventory Optimization",
    page_icon="📦",
    layout="wide"
    
)
render_sidebar()

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("data/inventory_recommendation.csv")

    df["Date"] = pd.to_datetime(df["Date"])

    return df

inventory = load_data()

# --------------------------------------------------
# KPI VALUES
# --------------------------------------------------

forecast_days = len(inventory)

avg_stock = inventory["Recommended_Stock"].mean()

max_stock = inventory["Recommended_Stock"].max()

avg_reorder = inventory["Reorder_Point"].mean()

avg_safety = inventory["Safety_Stock"].mean()

# --------------------------------------------------
# HERO
# --------------------------------------------------

st.markdown(
    """
<div style="background:linear-gradient(90deg,#059669,#047857); padding:28px; border-radius:22px; margin-bottom:20px;">

<h1 style="color:white; margin:0;">
📦 Inventory Optimization
</h1>

<p style="color:white; font-size:18px;">
Forecast-Based Inventory Planning & Stock Optimization
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

        "📅 Days",

        forecast_days

    )

with c2:

    st.metric(

        "📦 Avg Stock",

        f"{avg_stock:.0f}"

    )

with c3:

    st.metric(

        "🛡 Safety Stock",

        f"{avg_safety:.0f}"

    )

with c4:

    st.metric(

        "📍 Reorder Point",

        f"{avg_reorder:.0f}"

    )

with c5:

    st.metric(

        "📈 Max Stock",

        f"{max_stock:.0f}"

    )

st.divider()

# --------------------------------------------------
# RECOMMENDED STOCK
# --------------------------------------------------

fig = px.line(

    inventory,

    x="Date",

    y="Recommended_Stock",

    markers=True,

    title="📦 Recommended Inventory Trend",

    color_discrete_sequence=["#10B981"]

)

fig.update_layout(

    template="plotly_dark",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    height=500

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

# --------------------------------------------------
# SAFETY STOCK & REORDER POINT
# --------------------------------------------------

left,right=st.columns(2)

with left:

    fig2=px.area(

        inventory,

        x="Date",

        y="Safety_Stock",

        title="🛡 Safety Stock",

        color_discrete_sequence=["#22C55E"]

    )

    fig2.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        height=420

    )

    st.plotly_chart(

        fig2,

        use_container_width=True

    )

with right:

    fig3=px.area(

        inventory,

        x="Date",

        y="Reorder_Point",

        title="📍 Reorder Point",

        color_discrete_sequence=["#14B8A6"]

    )

    fig3.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        height=420

    )

    st.plotly_chart(

        fig3,

        use_container_width=True

    )

st.divider()
# --------------------------------------------------
# INVENTORY TABLE
# --------------------------------------------------

st.markdown("## 📋 Inventory Planning")

display = inventory.copy()

display["Forecast"] = display["Forecast"].round(2)
display["Safety_Stock"] = display["Safety_Stock"].round(2)
display["Reorder_Point"] = display["Reorder_Point"].round(2)
display["Recommended_Stock"] = display["Recommended_Stock"].round(2)

st.dataframe(

    display,

    use_container_width=True,

    hide_index=True

)

st.divider()

# --------------------------------------------------
# STOCK DISTRIBUTION
# --------------------------------------------------

fig4 = px.histogram(

    inventory,

    x="Recommended_Stock",

    nbins=25,

    title="📊 Recommended Stock Distribution",

    color_discrete_sequence=["#10B981"]

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
# BUSINESS SUMMARY
# --------------------------------------------------

left,right = st.columns(2)

with left:

    st.success(f"""

### 📦 Inventory Summary

📅 Forecast Days

**{forecast_days:,}**

📦 Average Stock

**{avg_stock:,.2f}**

🛡 Average Safety Stock

**{avg_safety:,.2f}**

""")

with right:

    st.info(f"""

### 📈 Planning Metrics

📍 Average Reorder Point

**{avg_reorder:,.2f}**

📈 Maximum Recommended Stock

**{max_stock:,.2f}**

""")

st.divider()

# --------------------------------------------------
# AI INVENTORY INSIGHTS
# --------------------------------------------------

st.markdown("## 🤖 AI Inventory Insights")

st.warning("""

### Recommendations

✅ Maintain safety stock to avoid stock-outs.

✅ Place replenishment orders before the reorder point.

✅ Use forecast trends to schedule purchasing.

✅ Monitor high-demand periods closely.

✅ Review inventory weekly and update forecasts.

""")

st.divider()

# --------------------------------------------------
# NEXT 7 DAYS PLAN
# --------------------------------------------------

st.markdown("## 📅 Next 7-Day Inventory Plan")

next7 = inventory.head(7)

st.dataframe(

    next7,

    use_container_width=True,

    hide_index=True

)

st.divider()

# --------------------------------------------------
# DOWNLOAD REPORT
# --------------------------------------------------

csv = inventory.to_csv(index=False).encode("utf-8")

st.download_button(

    "⬇ Download Inventory Report",

    csv,

    "inventory_report.csv",

    "text/csv"

)

st.divider()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""

<div class='footer'>

<h3 style="color:white;">

📦 Inventory Optimization

</h3>

RetailPulse AI

<br><br>

Developed by <b>Apeksha Kaushik</b>

</div>

""", unsafe_allow_html=True)