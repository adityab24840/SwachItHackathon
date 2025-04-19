import streamlit as st
import sys
import os
import random
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

# Use direct relative import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.calendar_widget import render_calendar_widget

def generate_reward_data(user_id):
    """Generate mock reward data for the user"""
    # Seed with user_id to get consistent results
    random.seed(hash(user_id))
    
    # Points based on days of proper disposal
    points = random.randint(75, 180)
    
    # Streak counts
    current_streak = random.randint(3, 14)
    longest_streak = max(current_streak, random.randint(7, 21))
    
    # Tax incentives based on points
    property_tax_rebate = min(10.0, points / 20)  # Max 10% rebate
    swm_discount = min(15.0, points / 15)  # Max 15% discount
    water_bill_discount = min(7.5, points / 25)  # Max 7.5% discount
    
    # Certificate eligibility
    certificate_eligible = points >= 100
    
    # Historical points
    months = ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr"]
    historical_points = [random.randint(50, 150) for _ in range(6)]
    
    # Achievement badges
    achievements = [
        {"name": "Waste Warrior", "earned": True, "date": "2025-03-15", "description": "Maintained 90%+ waste segregation compliance for a month"},
        {"name": "Compost Champion", "earned": points >= 100, "date": "2025-04-01" if points >= 100 else None, "description": "Successfully implemented home composting"},
        {"name": "Clean Street Leader", "earned": random.choice([True, False]), "date": "2025-02-22" if random.choice([True, False]) else None, "description": "Organized community clean-up drive"},
        {"name": "Zero Waste Household", "earned": False, "date": None, "description": "Achieved near-zero waste in household for 3 consecutive months"}
    ]
    
    return {
        "points": points,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "property_tax_rebate": property_tax_rebate,
        "swm_discount": swm_discount,
        "water_bill_discount": water_bill_discount,
        "certificate_eligible": certificate_eligible,
        "next_milestone": 100 if points < 100 else 200 if points < 200 else 300,
        "historical_points": {
            "months": months,
            "points": historical_points
        },
        "achievements": achievements
    }

def render():
    if "user" not in st.session_state:
        st.warning("Please login to view your rewards")
        st.session_state["page"] = "login"
        return
    
    user = st.session_state["user"]
    user_id = user.get("id", hash(user["username"]))
    
    st.title("BBMP नागरिक पुरस्कार कार्यक्रम / BBMP Citizen Rewards Program")
    
    # Get user's reward data
    rewards = generate_reward_data(user_id)
    
    # Display reward points prominently with BBMP branding
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1e3a8a 0%, #3949ab 100%); border-radius: 10px; padding: 20px; color: white; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="text-align: left; padding-left: 20px;">
                <img src="https://via.placeholder.com/60x60?text=BBMP" style="width: 60px; height: 60px; border-radius: 50%;">
            </div>
            <div style="flex-grow: 1;">
                <h2 style="color: white; margin-bottom: 5px;">Your SwachIT Points: {rewards['points']}</h2>
                <p style="margin: 0; opacity: 0.9;">Current streak: {rewards['current_streak']} days | Longest streak: {rewards['longest_streak']} days</p>
            </div>
            <div style="text-align: right; padding-right: 20px;">
                <p style="margin: 0;">Household ID: {user_id}</p>
                <p style="margin: 0;">Rank: {random.randint(1, 100)}/{random.randint(500, 1000)}</p>
            </div>
        </div>
        <div style="margin-top: 15px; background-color: rgba(255,255,255,0.2); border-radius: 5px; padding: 10px;">
            <p style="margin: 0;">Next reward at {rewards['next_milestone']} points ({rewards['next_milestone'] - rewards['points']} more to go)</p>
            <div style="background-color: rgba(255,255,255,0.3); border-radius: 10px; height: 10px; width: 100%; margin-top: 5px;">
                <div style="background-color: #4CAF50; border-radius: 10px; height: 10px; width: {min(100, (rewards['points'] / rewards['next_milestone']) * 100)}%;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Points history chart
    st.markdown("### Your Points History")
    
    # Create DataFrame for points history
    months = rewards["historical_points"]["months"]
    points = rewards["historical_points"]["points"]
    
    df_history = pd.DataFrame({
        "Month": months,
        "Points": points
    })
    
    # Create the chart
    fig = px.bar(
        df_history,
        x="Month",
        y="Points",
        title="",
        color_discrete_sequence=['#1e3a8a']
    )
    
    # Add average line
    avg_points = sum(points) / len(points)
    fig.add_hline(
        y=avg_points,
        line_dash="dot",
        annotation_text=f"Average: {avg_points:.1f} points",
        annotation_position="top right"
    )
    
    fig.update_layout(
        height=300,
        margin=dict(l=40, r=40, t=10, b=40)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Two-column layout for incentives and certificates
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # BBMP Tax Incentives section
        st.markdown("### BBMP Tax Incentives / कर प्रोत्साहन")
        
        incentives = [
            {
                "title": "Property Tax Rebate / संपत्ति कर में छूट",
                "value": f"{rewards['property_tax_rebate']:.1f}%",
                "details": "Applicable on your next property tax payment",
                "icon": "🏠",
                "code": f"PTR{random.randint(1000, 9999)}"
            },
            {
                "title": "SWM Charges Discount / SWM शुल्क में छूट",
                "value": f"{rewards['swm_discount']:.1f}%",
                "details": "On next quarter's solid waste management fees",
                "icon": "🗑️",
                "code": f"SWM{random.randint(1000, 9999)}"
            },
            {
                "title": "Water Bill Discount / पानी बिल में छूट",
                "value": f"{rewards['water_bill_discount']:.1f}%",
                "details": "Applicable on BWSSB charges for next 3 months",
                "icon": "💧",
                "code": f"WBD{random.randint(1000, 9999)}"
            }
        ]
        
        for incentive in incentives:
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin-bottom: 15px; display: flex; background-color: #f9f9f9;">
                <div style="font-size: 2em; margin-right: 15px; display: flex; align-items: center;">{incentive["icon"]}</div>
                <div style="flex-grow: 1;">
                    <h4 style="margin: 0;">{incentive["title"]}</h4>
                    <p style="color: #666; margin-top: 5px; margin-bottom: 5px;">{incentive["details"]}</p>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: bold; color: #1e3a8a; font-size: 1.2em;">{incentive["value"]}</span>
                        <span style="background-color: #e8f5e9; padding: 3px 10px; border-radius: 15px; font-size: 0.8em;">
                            Coupon Code: {incentive["code"]}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # How to redeem
        st.markdown("### How to Redeem / कैसे रिडीम करें")
        
        st.markdown("""
        <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; border-radius: 5px;">
            <h4 style="margin-top: 0;">Redemption Process:</h4>
            <ol style="margin-bottom: 0;">
                <li>Log in to <a href="https://bbmp.gov.in">BBMP citizen portal</a> with your registered credentials</li>
                <li>Navigate to "Tax & Payments" section</li>
                <li>Enter the coupon code when making payment</li>
                <li>Discount will be automatically applied to your bill</li>
                <li>For in-person redemption, visit your nearest BBMP Citizen Service Center</li>
            </ol>
            <p style="margin-top: 10px; margin-bottom: 0;"><strong>Note:</strong> Incentives are valid for 3 months from date of issue.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Swachhata Certificate
        st.markdown("### Swachhata Certificate / स्वच्छता प्रमाणपत्र")
        
        if rewards["certificate_eligible"]:
            st.markdown(f"""
            <div style="border: 2px solid #4CAF50; border-radius: 10px; padding: 15px; text-align: center; background-color: #f1f8e9;">
                <img src="https://via.placeholder.com/100x100?text=Certificate" style="width: 100px; height: 100px; margin-bottom: 10px;">
                <h4 style="margin: 0; color: #2E7D32;">Congratulations!</h4>
                <p>You are eligible for BBMP Swachhata Certificate</p>
                <p style="font-size: 0.8em; color: #666;">Certificate ID: BBMP-SWM-{random.randint(10000, 99999)}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.button("Download Certificate / प्रमाणपत्र डाउनलोड करें", key="download_certificate")
            st.button("Share on Social Media / सोशल मीडिया पर शेयर करें", key="share_certificate")
        else:
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; text-align: center; background-color: #f5f5f5;">
                <img src="https://via.placeholder.com/100x100?text=Certificate" style="width: 100px; height: 100px; margin-bottom: 10px; opacity: 0.5;">
                <h4 style="margin: 0; color: #666;">Almost there!</h4>
                <p>You need {100 - rewards['points']} more points to qualify for the Swachhata Certificate</p>
            </div>
            """, unsafe_allow_html=True)
            st.progress(rewards['points'] / 100)
        
        # Achievements and badges
        st.markdown("### Achievements / उपलब्धियां")
        
        for achievement in rewards["achievements"]:
            if achievement["earned"]:
                badge_style = "border: 2px solid #4CAF50; background-color: #f1f8e9;"
                badge_icon = "✅"
                badge_status = f"Earned on {achievement['date']}"
            else:
                badge_style = "border: 1px solid #ddd; background-color: #f5f5f5; opacity: 0.7;"
                badge_icon = "🔒"
                badge_status = "Locked - Keep segregating waste to unlock!"
            
            st.markdown(f"""
            <div style="{badge_style} border-radius: 10px; padding: 10px; margin-bottom: 10px; display: flex;">
                <div style="font-size: 1.5em; margin-right: 10px;">{badge_icon}</div>
                <div style="flex-grow: 1;">
                    <h4 style="margin: 0;">{achievement["name"]}</h4>
                    <p style="margin: 5px 0; font-size: 0.9em;">{achievement["description"]}</p>
                    <p style="margin: 0; font-size: 0.8em; color: #666;">{badge_status}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Waste disposal calendar
    st.markdown("---")
    st.markdown("### Your Waste Disposal Calendar")
    render_calendar_widget(user_id)
    
    # Neighborhood leaderboard
    st.markdown("---")
    st.markdown("### Neighborhood Leaderboard / पड़ोस लीडरबोर्ड")
    
    # Generate leaderboard data
    household_names = [
        user["username"], 
        "Kumar Residence", 
        "Sharma Family", 
        "Gupta House", 
        "Rao Household",
        "Patel Residence",
        "Singh Family",
        "Reddy House"
    ]
    
    np.random.seed(42)  # For consistent results
    leaderboard_points = np.random.randint(60, 200, len(household_names))
    
    # Make sure the current user is in the list with their actual points
    user_idx = 0  # First item is current user
    leaderboard_points[user_idx] = rewards["points"]
    
    # Sort by points
    leaderboard = sorted(zip(household_names, leaderboard_points), key=lambda x: x[1], reverse=True)
    
    # Create DataFrame
    df_leaderboard = pd.DataFrame({
        "Rank": range(1, len(leaderboard) + 1),
        "Household": [item[0] for item in leaderboard],
        "Points": [item[1] for item in leaderboard]
    })

    # Add a column to identify current user for styling
    df_leaderboard["IsCurrentUser"] = [household == household_names[0] for household in df_leaderboard["Household"]]

    # Display the DataFrame without the IsCurrentUser column
    st.dataframe(
        df_leaderboard.drop(columns=["IsCurrentUser"]).style.apply(
            lambda x: ["background-color: #e8f5e9" if df_leaderboard.iloc[i]["IsCurrentUser"] else "" 
                    for i in range(len(df_leaderboard))],
            axis=0
        ),
        hide_index=True,
        use_container_width=True
    )
        
    # How to earn more points
    st.markdown("---")
    st.markdown("### How to Earn More Points / ಹೆಚ್ಚಿನ ಅಂಕಗಳನ್ನು ಗಳಿಸುವುದು ಹೇಗೆ")  
    campaigns = [
    {
        "title": "Plastic-Free Bengaluru / ಪ್ಲಾಸ್ಟಿಕ್-ಮುಕ್ತ ಬೆಂಗಳೂರು",
        "description": "Join the plastic reduction initiative to earn bonus points and exclusive rewards.",
        "dates": "May 1 - June 30, 2025",
        "bonus": "+50 bonus points",
        "status": "Upcoming"
    },
    {
        "title": "Monsoon Readiness Drive / ಮುಂಗಾರು ಸಿದ್ಧತಾ ಅಭಿಯಾನ",
        "description": "Help prepare drains and waste systems for monsoon to prevent flooding.",
        "dates": "June 1 - June 15, 2025",
        "bonus": "+75 bonus points",
        "status": "Upcoming"
    }
]

      
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Regular Activities / नियमित गतिविधियाँ
        - **Daily waste segregation**: +5 points / day
        - **Weekly consistency bonus**: +10 points
        - **Monthly perfect record**: +50 points
        - **Reporting waste dumps**: +20 points per valid report
        - **Participating in clean-up drives**: +30 points
        """)
    
    with col2:
        st.markdown("""
        #### Special Initiatives / विशेष पहल
        - **Composting at home**: +20 points/month
        - **Plastic reduction initiatives**: +15 points
        - **Referring neighbors to SwachIT**: +25 points per sign-up
        - **Community clean-up organization**: +100 points
        - **Waste reduction workshops**: +40 points
        """)
    
    # Special campaigns section
    st.markdown("### Special Campaigns / विशेष अभियान")
    
    campaigns = [
        {
            "title": "Plastic-Free Bengaluru / प्लास्टिक-मुक्त बेंगलुरु",
            "description": "Join the plastic reduction initiative to earn bonus points and exclusive rewards.",
            "dates": "May 1 - June 30, 2025",
            "bonus": "+50 bonus points",
            "status": "Upcoming"
        },
        {
            "title": "Monsoon Readiness Drive / मानसून तैयारी अभियान",
            "description": "Help prepare drains and waste systems for monsoon to prevent flooding.",
            "dates": "June 1 - June 15, 2025",
            "bonus": "+75 bonus points",
            "status": "Upcoming"
        }
    ]
    
    col1, col2 = st.columns(2)
    
    for i, campaign in enumerate(campaigns):
        col = col1 if i % 2 == 0 else col2
        status_color = "#FFC107" if campaign["status"] == "Upcoming" else "#4CAF50"
        
        col.markdown(f"""
        <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; height: 200px; background-color: #f9f9f9;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0;">{campaign["title"]}</h4>
                <span style="background-color: {status_color}; color: white; padding: 3px 10px; border-radius: 15px; font-size: 0.8em;">
                    {campaign["status"]}
                </span>
            </div>
            <p style="margin: 10px 0;">{campaign["description"]}</p>
            <p><strong>Dates:</strong> {campaign["dates"]}</p>
            <p><strong>Reward:</strong> {campaign["bonus"]}</p>
            <button style="background-color: #1e3a8a; color: white; border: none; padding: 5px 15px; border-radius: 5px; cursor: pointer;">
                Sign Up
            </button>
        </div>
        """, unsafe_allow_html=True)
    
    # --- FOOTER ---
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8em;">
        © 2025 SwachIT - BBMP Rewards Program | Terms and Conditions Apply
        <br>
        For assistance: rewards.swachit@bbmp.gov.in | Toll-free: 1800-XXX-XXXX
    </div>
    """, unsafe_allow_html=True)