import streamlit as st
import sys
import os

# Use direct relative import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers.user_controller import login

def render():
    # Check if user is already logged in - redirect to dashboard in that case
    if "user" in st.session_state:
        # Instead of importing from app, directly update session state
        st.session_state["page"] = "dashboard"
        # Don't rerun here - it will be handled by main app
        return

    # Top header with government branding
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/en/thumb/6/69/BBMP_logo.png/220px-BBMP_logo.png", width=120)
    
    st.markdown("""
    # SwachIT - BBMP Smart Waste Management
    ಸ್ವಚ್ಛ ಬೆಂಗಳೂರು ಅಭಿಯಾನಕ್ಕೆ ಸ್ವಾಗತ / Welcome to Swachh Bengaluru Campaign
    ಬೃಹತ್ ಬೆಂಗಳೂರು ಮಹಾನಗರ ಪಾಲಿಕೆ (BBMP) ಜೊತೆಗೆ, ಡೇಟಾ-ಆಧಾರಿತ ಸ್ಮಾರ್ಟ್ ತ್ಯಾಜ್ಯ ನಿರ್ವಹಣೆ
    Data-driven smart waste management in partnership with Bruhat Bengaluru Mahanagara Palike
    """)
    
    with st.container():
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Government-style login form with border
            st.markdown("""
            <div style="border: 1px solid #ccc; border-radius: 5px; padding: 20px; background-color: #f9f9f9;">
                <h3 style="text-align: center; color: #1e3a8a;">Login / ಲಾಗಿನ್</h3>
            </div>
            """, unsafe_allow_html=True)
            
            username = st.text_input("Username / ಬಳಕೆದಾರ ಹೆಸರು", key="login_username")
            password = st.text_input("Password / ಪಾಸ್‌ವರ್ಡ್", type="password", key="login_password")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                login_clicked = st.button("Login / ಲಾಗಿನ್", key="login_button", use_container_width=True)
            
            if login_clicked:
                if username and password:
                    success, user = login(username, password)
                    if success:
                        # Store the user in session state
                        st.session_state["user"] = user
                        st.session_state["authenticated"] = True
                        st.session_state["page"] = "dashboard"
                        
                        # Show success message
                        st.success(f"ಸ್ವಾಗತ, {user['username']}! / Welcome, {user['username']}!")
                        
                        # Use a safer approach to redirect - set flag for main app to handle
                        st.session_state["redirect_to_dashboard"] = True
                        st.rerun()
                    else:
                        st.error("ಅಮಾನ್ಯ ಬಳಕೆದಾರ ಹೆಸರು ಅಥವಾ ಪಾಸ್‌ವರ್ಡ್ / Invalid username or password")
                else:
                    st.warning("ದಯವಿಟ್ಟು ಬಳಕೆದಾರ ಹೆಸರು ಮತ್ತು ಪಾಸ್‌ವರ್ಡ್ ಎರಡನ್ನೂ ನಮೂದಿಸಿ / Please enter both username and password")
                    
            # Replace the placeholder image (around line 66-68) with this more reliable solution:

        st.markdown("---")
        st.markdown("""
        ##### Cleanliness Map Preview / ಸ್ವಚ್ಛತೆ ನಕ್ಷೆ ಪೂರ್ವವೀಕ್ಷಣೆ
        """)

        # Create a simple map visualization using HTML/CSS instead of an external image
        st.markdown("""
        <div style="border: 1px solid #ccc; border-radius: 5px; padding: 5px; background-color: #f9f9f9; margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span style="font-size: 0.8em; color: #666;">Poor</span>
                <span style="font-size: 0.8em; color: #666;">Average</span>
                <span style="font-size: 0.8em; color: #666;">Good</span>
                <span style="font-size: 0.8em; color: #666;">Excellent</span>
            </div>
            <div style="display: flex; height: 10px; margin-bottom: 15px;">
                <div style="flex: 1; background-color: #e74c3c;"></div>
                <div style="flex: 1; background-color: #f39c12;"></div>
                <div style="flex: 1; background-color: #3498db;"></div>
                <div style="flex: 1; background-color: #2ecc71;"></div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px;">
                <div style="background-color: #f39c12; height: 60px; border-radius: 3px; display: flex; align-items: center; justify-content: center;">
                    <span style="color: white; font-weight: bold; font-size: 0.8em;">ಕೋರಮಂಗಲ</span>
                </div>
                <div style="background-color: #2ecc71; height: 60px; border-radius: 3px; display: flex; align-items: center; justify-content: center;">
                    <span style="color: white; font-weight: bold; font-size: 0.8em;">ಇಂದಿರಾನಗರ</span>
                </div>
                <div style="background-color: #3498db; height: 60px; border-radius: 3px; display: flex; align-items: center; justify-content: center;">
                    <span style="color: white; font-weight: bold; font-size: 0.8em;">ಜಯನಗರ</span>
                </div>
                <div style="background-color: #e74c3c; height: 60px; border-radius: 3px; display: flex; align-items: center; justify-content: center;">
                    <span style="color: white; font-weight: bold; font-size: 0.8em;">HSR ಲೇಔಟ್</span>
                </div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px; margin-top: 5px;">
                <div style="background-color: #3498db; height: 60px; border-radius: 3px; display: flex; align-items: center; justify-content: center;">
                    <span style="color: white; font-weight: bold; font-size: 0.8em;">ಮಲ್ಲೇಶ್ವರಂ</span>
                </div>
                <div style="background-color: #e74c3c; height: 60px; border-radius: 3px; display: flex; align-items: center; justify-content: center;">
                    <span style="color: white; font-weight: bold; font-size: 0.8em;">ಶಿವಾಜಿನಗರ</span>
                </div>
                <div style="background-color: #2ecc71; height: 60px; border-radius: 3px; display: flex; align-items: center; justify-content: center;">
                    <span style="color: white; font-weight: bold; font-size: 0.8em;">ಹೆಬ್ಬಾಳ</span>
                </div>
                <div style="background-color: #f39c12; height: 60px; border-radius: 3px; display: flex; align-items: center; justify-content: center;">
                    <span style="color: white; font-weight: bold; font-size: 0.8em;">ವೈಟ್‌ಫೀಲ್ಡ್</span>
                </div>
            </div>
        </div>
        <p style="text-align: center; color: #666; font-size: 0.8em;">Ward-level cleanliness visualization / ವಾರ್ಡ್-ಮಟ್ಟದ ಸ್ವಚ್ಛತೆ ದೃಶ್ಯೀಕರಣ</p>
        """, unsafe_allow_html=True)       
         
        with col2:
            st.markdown("""
            <div style="border: 1px solid #ccc; border-radius: 5px; padding: 20px; background-color: #f9f9f9;">
                <h3 style="color: #1e3a8a;">SwachIT Platform Features / ಪ್ಲಾಟ್‌ಫಾರ್ಮ್ ವೈಶಿಷ್ಟ್ಯಗಳು</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            ### Real-time Waste Mapping / ನೈಜ-ಸಮಯದ ತ್ಯಾಜ್ಯ ಮ್ಯಾಪಿಂಗ್

            **Track ward-level metrics:**
            - Color-coded ward-level cleanliness mapping / ವಾರ್ಡ್-ಮಟ್ಟದ ಸ್ವಚ್ಛತೆಯ ಬಣ್ಣ-ಕೋಡ್ ಮ್ಯಾಪಿಂಗ್
            - Real-time monitoring of waste hotspots / ತ್ಯಾಜ್ಯ ಹಾಟ್‌ಸ್ಪಾಟ್‌ಗಳ ನೈಜ-ಸಮಯದ ಮೇಲ್ವಿಚಾರಣೆ
            - Coverage of all Bengaluru areas including Koramangala, Indiranagar, Jayanagar / ಕೋರಮಂಗಲ, ಇಂದಿರಾನಗರ, ಜಯನಗರ ಸೇರಿದಂತೆ ಎಲ್ಲಾ ಬೆಂಗಳೂರು ಪ್ರದೇಶಗಳು

            ### Municipal Incentives / ಮುನ್ಸಿಪಲ್ ಪ್ರೋತ್ಸಾಹಧನಗಳು
            - 5-10% rebate on property tax / ಆಸ್ತಿ ತೆರಿಗೆಯಲ್ಲಿ 5-10% ರಿಯಾಯಿತಿ
            - Special concessions on SWM charges / SWM ಶುಲ್ಕಗಳಲ್ಲಿ ವಿಶೇಷ ರಿಯಾಯಿತಿಗಳು
            - BESCOM bill benefits / BESCOM ಬಿಲ್‌ಗಳ ಮೇಲೆ ಲಾಭಗಳು
            
            ### For testing / ಪರೀಕ್ಷೆಗಾಗಿ
            - Username / ಬಳಕೆದಾರ ಹೆಸರು: `demo`
            - Password / ಪಾಸ್‌ವರ್ಡ್: `password`
            """)
            
            st.info("For assistance, call BBMP helpline: 080-2596-1111")
    
    # G20-style footer section
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; font-size: 0.8em; color: #4b5563;">
            <p>SwachIT - An initiative under Swachh Bharat Mission & Smart Cities</p>
            <p>Developed in partnership with Ministry of Housing and Urban Affairs</p>
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg" width="50">
            <p>© 2025 ಬೃಹತ್ ಬೆಂಗಳೂರು ಮಹಾನಗರ ಪಾಲಿಕೆ (BBMP)</p>
        </div>
        """, unsafe_allow_html=True)