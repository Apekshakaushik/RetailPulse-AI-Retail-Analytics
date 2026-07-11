import streamlit as st


def render_sidebar():

    # --------------------------------------------------------
    # HIDE STREAMLIT'S DEFAULT AUTO-GENERATED PAGE NAV
    # (this is what was showing "app", "1 Sales Analytics", etc.)
    # --------------------------------------------------------
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] { display: none; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # BRANDING
    # --------------------------------------------------------
    st.sidebar.markdown(
        """
<div style="text-align:center;padding:14px 0 10px 0;">
  <div style="font-size:30px;">📊</div>
  <div style="color:white;font-size:19px;font-weight:800;margin-top:4px;">RetailPulse AI</div>
  <div style="color:#9CA3AF;font-size:12.5px;margin-top:2px;">AI-Powered Retail Intelligence</div>
</div>
<hr style="border:1px solid rgba(255,255,255,.08);margin:0 0 12px 0;">
""",
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # CUSTOM NAVIGATION (replaces default sidebar page list)
    # NOTE: adjust the paths below if your pages/ files are
    # named differently — must match the actual filenames.
    # --------------------------------------------------------
    st.sidebar.markdown(
        '<div style="color:#64748B;font-size:11.5px;font-weight:700;'
        'letter-spacing:1.5px;margin:4px 0 8px 4px;">NAVIGATION</div>',
        unsafe_allow_html=True,
    )

    st.sidebar.page_link("app.py", label="Home", icon="🏠")
    st.sidebar.page_link("pages/1_Sales_Analytics.py", label="Sales Analytics", icon="📊")
    st.sidebar.page_link("pages/2_Customer_Analytics.py", label="Customer Analytics", icon="👥")
    st.sidebar.page_link("pages/3_Demand_Forecasting.py", label="Demand Forecasting", icon="📈")
    st.sidebar.page_link("pages/4_Churn_Prediction.py", label="Churn Prediction", icon="⚠️")
    st.sidebar.page_link("pages/5_Inventory_Optimization.py", label="Inventory Optimization", icon="📦")
    st.sidebar.page_link("pages/6_About.py", label="About", icon="ℹ️")

    st.sidebar.markdown(
        '<hr style="border:1px solid rgba(255,255,255,.08);margin:16px 0;">',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------
    st.sidebar.markdown(
        """
<div style="text-align:center;padding-top:4px;">
  <div style="color:#9CA3AF;font-size:12px;">Developed by</div>
  <div style="color:#3B82F6;font-weight:700;font-size:13.5px;">Apeksha Kaushik</div>
</div>
""",
        unsafe_allow_html=True,
    )