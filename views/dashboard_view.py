import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os
import base64
import random
import plotly.io as pio
import plotly.figure_factory as ff
import plotly.io as pio
pio.templates.default = "plotly"

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers.waste_controller import get_waste_stats, get_active_complaints, get_ward_cleanliness_scores


def render():
    # Check if user is logged in
    if "user" not in st.session_state:
        st.warning("Please login to access the dashboard")
        st.session_state["page"] = "login"
        return
    
    user = st.session_state["user"]
    user_id = user.get("id", hash(user["username"]))
    user_ward = user.get("ward", "Koramangala")
    
    # Page title with BBMP branding
    st.markdown("""
    <div style="background-color: #0078D7; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center;">
            <div style="background-color: white; border-radius: 5px; padding: 5px; width: 80px; height: 80px; display: flex; align-items: center; justify-content: center; margin-right: 20px;">
                <div style="font-weight: bold; text-align: center; color: #0078D7; font-size: 24px;">BBMP</div>
            </div>
            <div>
                <h1 style="margin: 0;">BBMP Smart Waste Management Dashboard</h1>
                <p style="margin: 0;">ಬೃಹತ್ ಬೆಂಗಳೂರು ಮಹಾನಗರ ಪಾಲಿಕೆ ಸ್ಮಾರ್ಟ್ ತ್ಯಾಜ್ಯ ನಿರ್ವಹಣಾ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message with user info
    st.markdown(f"""
    <div style="background-color: #f0f7fa; padding: 15px; border-radius: 5px; border-left: 5px solid #0078D7; margin-bottom: 20px;">
        <h3>Welcome, {user.get('name', user['username'])}!</h3>
        <p>Ward: <b>{user_ward}</b> | User ID: {user_id}</p>
        <p>Last updated: {datetime.now().strftime('%d %B %Y, %H:%M')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get waste stats for this user and their ward
    user_stats, user_df = get_waste_stats(user_id, user_ward)
    ward_stats, ward_df = get_waste_stats(None, user_ward)
    
    # Create tabs for different dashboard sections
    tab1, tab2, tab3 = st.tabs(["Overview", "Waste Analytics", "Community Issues"])
    
    def get_ward_map_data():
        """
        Generate geospatial data for ward-level waste management performance
        In a real app, this would use actual GIS data for BBMP wards
        """
        # For demo purposes, we'll create mock lat/long coordinates for Bangalore wards
        bengaluru_center = [12.9716, 77.5946]  # Lat/Long for Bangalore
        
        wards = [
            "Koramangala", "Indiranagar", "Jayanagar", "JP Nagar", "HSR Layout", 
            "Malleswaram", "Shivajinagar", "Hebbal", "Yelahanka", "Mahadevpura",
            "Whitefield", "Electronic City"
        ]
        
        # Generate pseudo-random but consistent coordinates around Bangalore
        random.seed(42)  # For consistent results
        
        ward_data = []
        for i, ward in enumerate(wards):
            # Generate coordinates in a roughly circular pattern around Bangalore center
            angle = (i / len(wards)) * 2 * np.pi
            radius = random.uniform(0.01, 0.08)  # ~1-8km in degrees
            
            lat = bengaluru_center[0] + radius * np.sin(angle)
            lon = bengaluru_center[1] + radius * np.cos(angle)
            
            # Generate a realistic score between 40-95
            score = random.randint(40, 95)
            
            # Determine category based on score
            if score >= 80:
                category = "Excellent"
                color = "#2ecc71"
            elif score >= 60:
                category = "Good"
                color = "#3498db"
            elif score >= 40:
                category = "Average"
                color = "#f39c12"
            else:
                category = "Needs Improvement"
                color = "#e74c3c"
                
            # Generate waste data
            waste_collected = random.uniform(5, 15)  # tonnes per day
            segregation_rate = random.uniform(50, 95)  # percentage
            collection_efficiency = random.uniform(70, 99)  # percentage
            
            ward_data.append({
                "ward": ward,
                "latitude": lat,
                "longitude": lon,
                "score": score,
                "category": category,
                "color": color,
                "waste_collected": round(waste_collected, 1),
                "segregation_rate": round(segregation_rate, 1),
                "collection_efficiency": round(collection_efficiency, 1)
            })
        
        return ward_data
    
    with tab1:
        # Display key metrics in a grid
        st.markdown("### Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Your Waste Generated", 
                value=f"{user_stats.get('total_waste_kg', 0):.1f} kg",
                delta=f"{random.uniform(-0.5, 0.5):.1f} kg"
            )
        with col2:
            st.metric(
                label="Segregation Rate", 
                value=f"{user_stats.get('segregation_rate', 0):.1f}%", 
                delta=f"{random.uniform(-2, 5):.1f}%"
            )
        with col3:
            st.metric(
                label="Ward Average", 
                value=f"{ward_stats.get('daily_average_kg', ward_stats.get('avg_daily_waste', 0)):.1f} kg/day", 
                delta=None
            )
        with col4:
            # Calculate cleanliness score based on segregation and consistency
            cleanliness_score = int(user_stats.get('segregation_rate', 75) * 0.7 + random.uniform(60, 90) * 0.3)            
            st.metric(
                label="Cleanliness Score", 
                value=f"{cleanliness_score}/100", 
                delta=f"{random.randint(-3, 7)}"
            )
        
        # Display ward ranking
        st.markdown("### Ward Cleanliness Ranking")
        
        def get_score_color(score):
            if score >= 80:
                return "#2ecc71"  # Green for excellent
            elif score >= 60:
                return "#3498db"  # Blue for good
            elif score >= 40:
                return "#f39c12"  # Orange for average
            else:
                return "#e74c3c"  # Red for needs improvement

        # Get ward scores
        ward_scores = get_ward_cleanliness_scores()
        
        # Find user's ward
        user_ward_rank = next((w for w in ward_scores if w['ward'] == user_ward), None)
        if user_ward_rank:
            # Add color based on score
            user_ward_rank['color'] = get_score_color(user_ward_rank['score'])
            
            # Display user's ward prominently
            st.markdown(f"""
            <div style="background-color: #e6f7ff; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                <h4>Your Ward Ranking: {user_ward_rank['rank']} out of {len(ward_scores)}</h4>
                <div style="display: flex; align-items: center;">
                    <div style="width: 100px; height: 100px; border-radius: 50%; background-color: {user_ward_rank['color']}; 
                                display: flex; align-items: center; justify-content: center; margin-right: 20px;">
                        <span style="color: white; font-size: 24px; font-weight: bold;">{user_ward_rank['score']}</span>
                    </div>
                    <div>
                        <p>Ward: <b>{user_ward}</b></p>
                        <p>Category: <b>{user_ward_rank['category']}</b></p>
                        <p>Change from last month: <b>{user_ward_rank['change']:+.1f}%</b></p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
        # Display all wards ranking in a table
        col1, col2 = st.columns([2, 3])
        
        with col1:
            st.markdown("#### All Wards")
            # Convert to DataFrame for display
            df_ranks = pd.DataFrame(ward_scores)
            # Highlight user's ward
            def highlight_user_ward(row):
                if row['ward'] == user_ward:
                    return ['background-color: #e6f7ff'] * len(row)
                return [''] * len(row)
            
            st.dataframe(
                df_ranks[['rank', 'ward', 'score', 'category', 'change']],
                use_container_width=True,
                hide_index=True
            )
        
        # Replace the map visualization section (around line 175-226) with this updated code:


        with col2:
            st.markdown("#### Ward-level Waste Management Performance")
            
            # Get ward map data
            ward_map_data = get_ward_map_data()
            
            # Create map visualization
            try:
                # Convert to DataFrame for Plotly
                df_map = pd.DataFrame(ward_map_data)
                
                # Create a hover text column
                df_map['hover_text'] = df_map.apply(
                    lambda row: f"<b>{row['ward']}</b><br>" + 
                            f"Score: {row['score']}/100<br>" +
                            f"Category: {row['category']}<br>" +
                            f"Waste: {row['waste_collected']} tonnes/day<br>" +
                            f"Segregation: {row['segregation_rate']}%",
                    axis=1
                )
                
                # Create the map with Mapbox token (important for display)
                fig = px.scatter_mapbox(
                    df_map,
                    lat="latitude",
                    lon="longitude",
                    hover_name="ward",
                    hover_data={"latitude": False, "longitude": False},
                    custom_data=["hover_text"],
                    color="score",
                    size="waste_collected",
                    size_max=15,
                    zoom=11,
                    mapbox_style="open-street-map",  # Changed to open-street-map which doesn't require a token
                    color_continuous_scale=[(0, "#e74c3c"), (0.5, "#f39c12"), (0.75, "#3498db"), (1, "#2ecc71")],
                    range_color=[30, 100]
                )
                
                # Set hover template
                fig.update_traces(
                    hovertemplate="%{customdata[0]}<extra></extra>"
                )
                
                # Update layout
                fig.update_layout(
                    height=350,
                    margin={"r":0,"t":0,"l":0,"b":0},
                    coloraxis_colorbar=dict(
                        title="Score",
                        tickvals=[40, 60, 80],
                        ticktext=["Poor", "Average", "Good"]
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                # Display more specific error for debugging
                st.error(f"Map error: {str(e)}")
                
                # Fallback to simple visualization
                st.markdown("#### Ward Cleanliness Scores")
                
                # Create simple colored bar chart as fallback
                fig = px.bar(
                    ward_scores, 
                    x='ward', 
                    y='score',
                    color='score',
                    color_continuous_scale=[(0, 'red'), (0.4, 'yellow'), (0.6, 'blue'), (1, 'green')],
                    labels={'ward': 'Ward', 'score': 'Cleanliness Score'},
                    title='Ward Cleanliness Scores'
                )
                
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)
        
        
        # Quick tips section
        st.markdown("### Waste Management Tips")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; height: 200px;">
                <h4 style="color: #0078D7;">Segregation Reminder</h4>
                <p>BBMP requires waste segregation into:</p>
                <ul>
                    <li><b>Green bin:</b> Organic/kitchen waste</li>
                    <li><b>Blue bin:</b> Recyclable waste</li>
                    <li><b>Red bin:</b> Hazardous waste</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; height: 200px;">
                <h4 style="color: #0078D7;">Collection Schedule</h4>
                <p>For ward: <b>Koramangala</b></p>
                <ul>
                    <li><b>Wet waste:</b> Daily 7am - 9am</li>
                    <li><b>Dry waste:</b> Wednesday, Saturday</li>
                    <li><b>Hazardous waste:</b> Last Saturday</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; height: 200px;">
                <h4 style="color: #0078D7;">Municipal Support</h4>
                <p><b>BBMP Helpline:</b> 080-22660000</p>
                <p><b>Waste Collection Issues:</b> 1533</p>
                <p><b>WhatsApp:</b> 8884477455</p>
                <p><b>Email:</b> swmbbmp@gmail.com</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Your Waste Analytics")
        
        # Create waste type breakdown - safely handle missing keys
        if 'by_type' in user_stats:
            waste_by_type = pd.DataFrame([{
                'type': waste_type,
                'amount': stats['amount_kg'],
                'segregated_pct': stats['segregated'] * 100
            } for waste_type, stats in user_stats['by_type'].items()])
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                # Create pie chart for waste composition
                fig = px.pie(
                    waste_by_type, 
                    values='amount', 
                    names='type',
                    title='Your Waste Composition',
                    color='type',
                    color_discrete_map={
                        'Wet': '#66c2a5',
                        'Dry': '#fc8d62',
                        'Hazardous': '#e78ac3',
                        'E-waste': '#8da0cb',
                        'Garden': '#a6d854'
                    }
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Create bar chart for segregation rates
                fig = px.bar(
                    waste_by_type,
                    x='type',
                    y='segregated_pct',
                    title='Segregation Rate by Waste Type',
                    labels={'segregated_pct': 'Segregation %', 'type': 'Waste Type'},
                    color='type',
                    color_discrete_map={
                        'Wet': '#66c2a5',
                        'Dry': '#fc8d62',
                        'Hazardous': '#e78ac3',
                        'E-waste': '#8da0cb',
                        'Garden': '#a6d854'
                    }
                )
                fig.update_layout(yaxis_range=[0, 100])
                
                # Add target line
                fig.add_shape(
                    type="line",
                    x0=-0.5,
                    x1=4.5,
                    y0=90,
                    y1=90,
                    line=dict(color="red", width=2, dash="dash"),
                )
                fig.add_annotation(
                    x=2,
                    y=92,
                    text="BBMP Target: 90%",
                    showarrow=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Add time series analysis
            st.markdown("### Waste Generation Trends")
            
            if 'time_series' in user_stats and user_stats['time_series']:
                try:
                    # Create time series DataFrame
                    time_series_df = pd.DataFrame(user_stats['time_series'])
                    time_series_df['date'] = pd.to_datetime(time_series_df['date'])
                    
                    # Group by date and type to get daily waste by type
                    daily_by_type = time_series_df.groupby(['date', 'type'])['amount_kg'].sum().reset_index()
                    
                    # Create stacked area chart
                    fig = px.area(
                        daily_by_type,
                        x='date',
                        y='amount_kg',
                        color='type',
                        title='Daily Waste Generation by Type (Last 30 Days)',
                        labels={'amount_kg': 'Waste (kg)', 'date': 'Date', 'type': 'Waste Type'},
                        color_discrete_map={
                            'Wet': '#66c2a5',
                            'Dry': '#fc8d62',
                            'Hazardous': '#e78ac3',
                            'E-waste': '#8da0cb',
                            'Garden': '#a6d854'
                        }
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Add day of week analysis
                    st.markdown("### Waste by Day of Week")
                    
                    # Add day of week
                    time_series_df['day_of_week'] = time_series_df['date'].dt.day_name()
                    time_series_df['day_num'] = time_series_df['date'].dt.dayofweek
                    
                    # Order days correctly
                    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    
                    # Group by day of week
                    day_summary = time_series_df.groupby(['day_of_week', 'day_num'])['amount_kg'].sum().reset_index()
                    day_summary = day_summary.sort_values('day_num')
                    
                    # Create bar chart
                    fig = px.bar(
                        day_summary,
                        x='day_of_week',
                        y='amount_kg',
                        title='Average Waste Generation by Day of Week',
                        labels={'amount_kg': 'Waste (kg)', 'day_of_week': 'Day'},
                        category_orders={'day_of_week': day_order},
                        color='amount_kg',
                        color_continuous_scale=[(0, '#2ecc71'), (1, '#e74c3c')]
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.info("💡 **Insight:** Weekends typically show higher waste generation. Consider additional collection services on these days.")
                    
                except Exception as e:
                    st.warning(f"Could not generate time series visualizations: {str(e)}")
            else:
                st.info("Time series data not available for this user or ward.")
        else:
            st.warning("Detailed waste type data is not available for this user or ward.")
    
    with tab3:
        st.markdown("### Community Waste Issues")
        
        # Active complaints in the ward
        complaints = get_active_complaints(user_ward)
        
        # Create tabs for viewing and reporting
        issue_tab1, issue_tab2 = st.tabs(["View Active Issues", "Report New Issue"])
        
        with issue_tab1:
            st.markdown(f"#### Active Complaints in {user_ward}")
            
            if not complaints:
                st.info("No active complaints in your ward currently.")
            else:
                # Create expandable list of complaints
                for i, complaint in enumerate(complaints):
                    with st.expander(f"{complaint['type']} at {complaint['location']} ({complaint['status']})"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"**ID:** {complaint['id']}")
                            reported_date = datetime.strptime(complaint.get('date_reported', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d')
                            days_open = complaint.get('age_days', 0)
                            st.markdown(f"**Reported:** {reported_date.strftime('%d %b %Y')} ({days_open} days ago)")
                            st.markdown(f"**Status:** {complaint['status']}")
                            st.markdown(f"**Priority:** {complaint['priority']}")
                            st.markdown(f"**Community Votes:** {complaint.get('votes', random.randint(0, 15))}")                        
                        with col2:
                            # Show action buttons
                            st.button(f"👍 Upvote", key=f"upvote_{i}")
                            st.button(f"📝 Add Comment", key=f"comment_{i}")
                            if complaint['status'] in ['Pending', 'In Progress']:
                                st.button(f"📞 Follow Up", key=f"follow_{i}")
                
                # Add summary metrics
                st.markdown("#### Issue Summary")
                
                col1, col2, col3, col4 = st.columns(4)
                
                # Calculate issue stats
                total_issues = len(complaints)
                pending_issues = sum(1 for c in complaints if c['status'] == 'Pending')
                resolved_issues = sum(1 for c in complaints if c['status'] == 'Resolved')
                high_priority = sum(1 for c in complaints if c['priority'] == 'High')
                
                col1.metric("Total Issues", total_issues)
                col2.metric("Pending", pending_issues, f"{pending_issues/total_issues*100:.0f}%")
                col3.metric("Resolved", resolved_issues, f"{resolved_issues/total_issues*100:.0f}%")
                col4.metric("High Priority", high_priority, f"{high_priority/total_issues*100:.0f}%")
                
                # Create issue heatmap by location
                st.markdown("#### Issue Distribution")
                
                try:
                    # Group complaints by location
                    location_count = {}
                    for complaint in complaints:
                        loc = complaint['location'].split(',')[0].strip()  # Get first part before comma
                        if loc in location_count:
                            location_count[loc] += 1
                        else:
                            location_count[loc] = 1
                    
                    # Convert to DataFrame for visualization
                    df_loc = pd.DataFrame({
                        'location': list(location_count.keys()),
                        'count': list(location_count.values())
                    }).sort_values('count', ascending=False)
                    
                    # Create bar chart
                    fig = px.bar(
                        df_loc,
                        x='location',
                        y='count',
                        title=f'Issue Distribution by Location in {user_ward}',
                        color='count',
                        color_continuous_scale=[(0, '#3498db'), (1, '#e74c3c')],
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                except Exception as e:
                    st.warning(f"Could not generate location distribution chart: {str(e)}")
        
        with issue_tab2:
            st.markdown("#### Report a New Waste Management Issue")
            
            # Create form for reporting
            with st.form(key="report_issue_form"):
                issue_type = st.selectbox(
                    "Type of Issue",
                    [
                        "Garbage not collected",
                        "Black spot/dumping",
                        "Overflowing bin",
                        "Segregation not enforced",
                        "Improper waste disposal",
                        "Burning of waste",
                        "Missing community bin",
                        "Other"
                    ]
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    location = st.text_input("Specific Location (address/landmark)")
                with col2:
                    ward = st.selectbox("Ward", ["Koramangala", "Indiranagar", "Jayanagar", "Other"], index=0)
                
                description = st.text_area("Detailed Description", height=100)
                
                col1, col2 = st.columns(2)
                with col1:
                    contact = st.text_input("Contact Number (optional)")
                with col2:
                    priority = st.select_slider("Priority", options=["Low", "Medium", "High"])
                
                photo = st.file_uploader("Upload Photo (optional)", type=["jpg", "jpeg", "png"])
                
                submit_button = st.form_submit_button("Submit Complaint")
                
                if submit_button:
                    if location and description:
                        # In a real app, this would call an API
                        st.success(f"""
                        Complaint registered successfully!
                        
                        Tracking ID: BBMP-{random.randint(1000, 9999)}
                        
                        A BBMP official will respond within 24-48 hours.
                        """)
                    else:
                        st.error("Please provide location and description to submit a complaint.")
    
    # Footer with BBMP branding
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>SwachIT | BBMP Smart Waste Management System</p>
        <p style="font-size: 0.8em;">© Bruhat Bengaluru Mahanagara Palike (BBMP) 2025</p>
    </div>
    """, unsafe_allow_html=True)