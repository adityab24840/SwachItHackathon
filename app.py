import streamlit as st
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up the page configuration - MUST be the first st command
st.set_page_config(
    page_title="SwachIT - BBMP Smart Waste Management",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create the sidebar title with reliable HTML formatting
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <h2 style="color: #0078D7; margin-bottom: 0;">SwachIT</h2>
    <p style="margin-top: 0;">BBMP Smart Waste Management</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "page" not in st.session_state:
    st.session_state["page"] = "login"
if "sidebar_rendered" not in st.session_state:
    st.session_state["sidebar_rendered"] = False
if "notifications" not in st.session_state:
    st.session_state["notifications"] = []

# Function to change pages
def set_page(page_name):
    st.session_state["page"] = page_name
    logger.info(f"Page changed to: {page_name}")

# Now import your views - AFTER defining set_page
from views import login_view, dashboard_view, metrics_view, rewards_view

# Handle redirection from login page
if "redirect_to_dashboard" in st.session_state and st.session_state["redirect_to_dashboard"]:
    st.session_state["page"] = "dashboard"
    st.session_state["redirect_to_dashboard"] = False

# Create sidebar with navigation and branding
with st.sidebar:
    
    # Define navigation options based on authentication status
    if "user" in st.session_state:
        # Show user info
        st.success(f"Logged in as: {st.session_state['user']['username']}")
        st.markdown(f"Ward: **{st.session_state['user'].get('ward', 'Koramangala')}**")
        
        # Navigation for authenticated users
        page = st.radio(
            "Navigation",
            ["Dashboard", "Metrics", "Rewards", "Logout"],
            key="sidebar_nav_auth"
        )
        
        if page == "Dashboard":
            st.session_state["page"] = "dashboard"
        elif page == "Metrics":
            st.session_state["page"] = "metrics"
        elif page == "Rewards":
            st.session_state["page"] = "rewards"
        elif page == "Logout":
            # Handle logout
            st.session_state.pop("user", None)
            st.session_state.pop("authenticated", None)
            st.session_state["page"] = "login"
            st.rerun()
    else:
        # Navigation for unauthenticated users
        page = st.radio(
            "Navigation",
            ["Login"],
            key="sidebar_nav_unauth"
        )
        st.session_state["page"] = "login"
        
        # Add some info for unauthenticated users
        st.info("Please log in to access all features")
    
    # Common footer elements
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.8em;">
    <strong>Important Links:</strong><br>
    <a href="https://bbmp.gov.in" target="_blank">BBMP Official Website</a><br>
    <a href="https://bbmp.gov.in/en/solid-waste-management/" target="_blank">SWM Portal</a><br>
    <a href="tel:+918025961111">Helpline: 080-2596-1111</a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("© 2025 Bruhat Bengaluru Mahanagara Palike")
    st.caption("Version 1.0.5")

# Render the appropriate view based on session state
if st.session_state["page"] == "login":
    login_view.render()
elif st.session_state["page"] == "dashboard":
    dashboard_view.render()
elif st.session_state["page"] == "metrics":
    metrics_view.render()
elif st.session_state["page"] == "rewards":
    rewards_view.render()