import streamlit as st
from pathlib import Path


def _load_css():
    css_file = Path("assets/style.css")
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def require_login():
    """
    Call this at the very top of every page (Home + all pages/*.py),
    right after st.set_page_config(). If the visitor hasn't submitted
    Name + Email yet, this renders the lock screen and stops the page
    from rendering anything further — no matter which page they land on.
    """

    _load_css()

    if "user_authenticated" not in st.session_state:
        st.session_state.user_authenticated = False

    if st.session_state.user_authenticated:
        return  # already logged in — let the page continue normally

    st.markdown(
        """
<div class="hero-card" style="text-align:center;">
  <div class="hero-eyebrow" style="justify-content:center;display:flex;">RETAILPULSE AI</div>
  <h1 class="hero-title">Enterprise Retail Intelligence Platform</h1>
  <p class="hero-subtitle" style="margin-left:auto;margin-right:auto;text-align:center;">
    Turning raw transaction data into revenue-driving decisions.
  </p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="auth-card">
  <div class="auth-icon">🔒</div>
  <div class="auth-title">System Authentication Required</div>
  <div class="auth-sub">Provide your name and email to unlock secure access</div>
</div>
""",
        unsafe_allow_html=True,
    )

    _, mid, _ = st.columns([1, 1.4, 1])
    with mid:
        with st.form("auth_form", clear_on_submit=False):
            full_name = st.text_input("Full Name", placeholder="e.g., John Doe")
            email = st.text_input("Email ID", placeholder="e.g., john.doe@company.com")
            submitted = st.form_submit_button("Unlock Dashboard →", use_container_width=True)

            if submitted:
                name_ok = bool(full_name.strip())
                email_ok = "@" in email and "." in email.split("@")[-1] and len(email.strip()) > 5

                if not name_ok:
                    st.error("Please enter your full name.")
                elif not email_ok:
                    st.error("Please enter a valid email address.")
                else:
                    st.session_state.user_authenticated = True
                    st.session_state.user_name = full_name.strip()
                    st.session_state.user_email = email.strip()
                    st.rerun()

    st.stop()  # nothing below this runs until authenticated