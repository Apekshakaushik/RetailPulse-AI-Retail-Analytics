import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib
from components.sidebar import render_sidebar

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Churn Prediction",
    page_icon="⚠️",
    layout="wide"
)
render_sidebar()
# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

@st.cache_resource
def load_model():

    return joblib.load("models/churn_model.pkl")

model = load_model()

# --------------------------------------------------
# HERO
# --------------------------------------------------

st.markdown(
    """
<div style="background:linear-gradient(90deg,#dc2626,#991b1b); padding:28px; border-radius:22px; margin-bottom:20px;">

<h1 style="color:white; margin:0;">
⚠️ Customer Churn Prediction
</h1>

<p style="color:white; font-size:18px;">
Predict customer churn using Random Forest Machine Learning.
</p>

</div>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# INPUT FORM
# --------------------------------------------------

st.markdown("## 📝 Customer Information")

left,right = st.columns(2)

with left:

    recency = st.slider(

        "📅 Recency",

        0,

        365,

        30

    )

    frequency = st.slider(

        "🛒 Frequency",

        1,

        100,

        5

    )

with right:

    monetary = st.number_input(

        "💰 Monetary (£)",

        min_value=0.0,

        value=1000.0,

        step=100.0

    )

    st.info("""

### Model Inputs

📅 Recency

🛒 Frequency

💰 Monetary

""")

st.divider()

# --------------------------------------------------
# PREDICT BUTTON
# --------------------------------------------------

predict = st.button(

    "🔮 Predict Customer Churn"

)

if predict:

    sample = np.array([

        [

            recency,

            frequency,

            monetary

        ]

    ])

    prediction = model.predict(sample)[0]

    probability = model.predict_proba(sample)[0]

    churn_probability = probability[1] * 100

    retention_probability = probability[0] * 100
        # --------------------------------------------------
    # RESULT
    # --------------------------------------------------

    st.divider()

    st.markdown("## 🎯 Prediction Result")

    if prediction == 1:

        st.error("""

# ⚠️ HIGH CHURN RISK

This customer is likely to churn.

""")

        risk_color = "#DC2626"
        risk_value = churn_probability

    else:

        st.success("""

# ✅ LOW CHURN RISK

This customer is likely to stay.

""")

        risk_color = "#10B981"
        risk_value = retention_probability

    # --------------------------------------------------
    # GAUGE CHART
    # --------------------------------------------------

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=risk_value,

            number={"suffix":"%"},

            title={"text":"Risk Score"},

            gauge={

                "axis":{"range":[0,100]},

                "bar":{"color":risk_color},

                "steps":[

                    {"range":[0,40],"color":"#10B981"},

                    {"range":[40,70],"color":"#FACC15"},

                    {"range":[70,100],"color":"#DC2626"}

                ]

            }

        )

    )

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        height=400

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    # --------------------------------------------------
    # PROBABILITY
    # --------------------------------------------------

    st.markdown("## 📊 Prediction Probability")

    p1,p2 = st.columns(2)

    with p1:

        st.metric(

            "⚠️ Churn Probability",

            f"{churn_probability:.2f}%"

        )

        st.progress(

            float(churn_probability/100)

        )

    with p2:

        st.metric(

            "✅ Retention Probability",

            f"{retention_probability:.2f}%"

        )

        st.progress(

            float(retention_probability/100)

        )

    st.divider()

    # --------------------------------------------------
    # CUSTOMER REPORT
    # --------------------------------------------------

    report = pd.DataFrame({

        "Recency":[recency],

        "Frequency":[frequency],

        "Monetary":[monetary],

        "Prediction":[

            "High Risk"

            if prediction==1

            else

            "Low Risk"

        ],

        "Churn Probability (%)":[

            round(churn_probability,2)

        ],

        "Retention Probability (%)":[

            round(retention_probability,2)

        ]

    })

    st.markdown("## 📋 Prediction Report")

    st.dataframe(

        report,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # --------------------------------------------------
    # AI RECOMMENDATIONS
    # --------------------------------------------------

    st.markdown("## 🤖 AI Recommendations")

    if prediction == 1:

        st.warning("""

### Recommended Actions

✅ Offer personalized discounts

✅ Send reminder emails

✅ Launch loyalty campaigns

✅ Contact customer through CRM

✅ Recommend frequently purchased products

""")

    else:

        st.success("""

### Recommended Actions

✅ Reward customer loyalty

✅ Upsell premium products

✅ Cross-sell related items

✅ Continue personalized marketing

✅ Maintain engagement through offers

""")

    st.divider()

    # --------------------------------------------------
    # DOWNLOAD REPORT
    # --------------------------------------------------

    csv = report.to_csv(index=False).encode("utf-8")

    st.download_button(

        "⬇ Download Prediction Report",

        csv,

        "churn_prediction_report.csv",

        "text/csv"

    )

st.divider()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""

<div class='footer'>

<h3 style='color:white;'>

⚠️ Customer Churn Prediction

</h3>

RetailPulse AI

<br><br>

Developed by <b>Apeksha Kaushik</b>

</div>

""",unsafe_allow_html=True)