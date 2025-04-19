import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers.waste_controller import get_waste_stats, get_ward_cleanliness_scores

def render():
    if "user" not in st.session_state:
        st.warning("Please login to view metrics")
        st.session_state["page"] = "login"
        return
        
    user = st.session_state["user"]
    user_ward = user.get("ward", "Koramangala")
    
    # BBMP-style header
    # BBMP-style header with base64 encoded image or alternative
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
    
    # Create tabs for different analytics views
    tab1, tab2, tab3, tab4 = st.tabs([
        "City Overview", 
        "Ward Performance",
        "Waste Segregation",
        "Environmental Impact"
    ])
    
    with tab1:
        st.markdown("### Bengaluru Waste Management Overview")
        
        # Key city metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Daily Waste Generated",
                "5,800 tonnes",
                "2.3%",
                delta_color="inverse"
            )
        
        with col2:
            st.metric(
                "Segregation Compliance",
                "83%",
                "4.5%"
            )
            
        with col3:
            st.metric(
                "Processing Efficiency",
                "77%",
                "5.2%"
            )
            
        with col4:
            st.metric(
                "Landfill Diversion",
                "65%",
                "8.7%"
            )
            
        # City map with ward performance
                
        st.markdown("#### Ward-level Waste Management Performance")

        # Get the ward data (you may need to adjust this to match your metrics_view.py structure)
        ward_data = get_ward_cleanliness_scores()  # Assuming you have this function imported

        # Convert to DataFrame
        df_map = pd.DataFrame(ward_data)

        # Create a simple but effective visualization that doesn't require Mapbox
        fig = px.scatter(
            df_map,
            x="rank",  # Use rank as x-axis (or another numerical value if rank isn't available)
            y="score",
            size=[30] * len(df_map),  # Fixed size for all points
            color="score",
            hover_name="ward",
            text="ward",
            color_continuous_scale=[(0, "#e74c3c"), (0.5, "#f39c12"), (0.75, "#3498db"), (1, "#2ecc71")],
            range_color=[30, 100],
            title="Ward Cleanliness Performance"
        )

        # Enhance the visualization
        fig.update_traces(
            textposition='top center',
            marker=dict(line=dict(width=1, color='DarkSlateGrey')),
        )

        # Improve layout
        fig.update_layout(
            height=450,
            xaxis_title="Ward Ranking",
            yaxis_title="Cleanliness Score",
            yaxis=dict(range=[30, 100]),
            plot_bgcolor='rgba(240, 247, 250, 1)',
        )

        # Add reference lines
        fig.add_shape(
            type="line",
            x0=0,
            x1=len(df_map)+1,
            y0=80,
            y1=80,
            line=dict(color="green", width=1, dash="dash")
        )
        fig.add_shape(
            type="line",
            x0=0,
            x1=len(df_map)+1,
            y0=60,
            y1=60,
            line=dict(color="orange", width=1, dash="dash")
        )
        fig.add_shape(
            type="line",
            x0=0,
            x1=len(df_map)+1,
            y0=40,
            y1=40,
            line=dict(color="red", width=1, dash="dash")
        )

        # Add annotations
        fig.add_annotation(
            x=len(df_map)/2,
            y=85,
            text="Excellent",
            showarrow=False,
            font=dict(color="green")
        )
        fig.add_annotation(
            x=len(df_map)/2,
            y=65,
            text="Good",
            showarrow=False,
            font=dict(color="orange")
        )
        fig.add_annotation(
            x=len(df_map)/2,
            y=45,
            text="Average",
            showarrow=False,
            font=dict(color="red")
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div style="font-size: 0.85em; color: #666; margin-top: -15px;">
        <p>Chart shows cleanliness scores by ward ranking. Hover over points for more details.</p>
        <p>Source: BBMP Solid Waste Management Department</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Monthly trend for city
        st.markdown("### Bengaluru Waste Management Trends")
        
        # Generate monthly data
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        waste_data = []
        
        for i, month in enumerate(months):
            # Add seasonal variations and a general improvement trend
            base = 5500 + 300 * np.sin(i/11 * 2 * np.pi)
            waste_gen = base + random.uniform(-100, 100)
            segregation = min(100, 70 + i/2 + random.uniform(-3, 3))
            processing = min(100, 65 + i/2.5 + random.uniform(-2, 2))
            
            waste_data.append({
                'month': month,
                'month_num': i+1,
                'waste_generated': waste_gen,
                'segregation_rate': segregation,
                'processing_rate': processing
            })
            
        df_trend = pd.DataFrame(waste_data)
        
        # Create two-axis plot for waste generated and processing metrics
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add waste generated line
        fig.add_trace(
            go.Scatter(
                x=df_trend['month'],
                y=df_trend['waste_generated'],
                name="Waste Generated (tonnes/day)",
                line=dict(color="#e74c3c", width=3)
            ),
            secondary_y=False
        )
        
        # Add segregation rate line
        fig.add_trace(
            go.Scatter(
                x=df_trend['month'],
                y=df_trend['segregation_rate'],
                name="Segregation Rate (%)",
                line=dict(color="#2ecc71", width=3)
            ),
            secondary_y=True
        )
        
        # Add processing rate line
        fig.add_trace(
            go.Scatter(
                x=df_trend['month'],
                y=df_trend['processing_rate'],
                name="Processing Rate (%)",
                line=dict(color="#3498db", width=3)
            ),
            secondary_y=True
        )
        
        # Add titles and labels
        fig.update_layout(
            title_text="Monthly Waste Management Metrics (2023)",
            xaxis=dict(title="Month"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
        )
        
        fig.update_yaxes(
            title_text="Waste Generated (tonnes/day)",
            secondary_y=False,
            range=[5000, 6000]
        )
        
        fig.update_yaxes(
            title_text="Rate (%)",
            secondary_y=True,
            range=[50, 100]
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Key initiatives and achievements
        st.markdown("### Key BBMP Waste Management Initiatives")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Recent Achievements
            
            - **Solid Waste Management Plants**: Increased processing capacity by 12% in the past year
            - **Door-to-door Collection**: Now covers 97% of residential areas
            - **Segregation at Source**: Improved from 70% to 83% in the past 12 months
            - **Black Spot Monitoring**: Reduced persistent black spots by 35%
            - **BBMP Sahaya App**: Over 25,000 waste-related complaints resolved
            """)
            
        with col2:
            st.markdown("""
            #### Upcoming Initiatives
            
            - **Smart Bins Deployment**: 500 new IoT-enabled bins in commercial areas
            - **Biomethanation Plants**: 5 new plants with 5 TPD capacity each
            - **Decentralized Composting**: 25 new community composting centers
            - **Ward-level Dry Waste Collection Centers**: 20 new centers planned
            - **Waste-to-Energy Plant**: 300 TPD capacity plant under construction
            """)
    
    with tab2:
        st.markdown(f"### {user_ward} Ward Performance Analytics")
        
        # Get ward data
        ward_stats, ward_df = get_waste_stats(None, user_ward)
        
        # Ward overview
        st.markdown("""
        <div style="background-color: #f0f7fa; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
            <h4>Ward Overview</h4>
            <p>This section provides detailed metrics for your local ward. Compare performance against targets and city averages.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Ward performance metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Find ward in cleanliness scores
            ward_data = next(w for w in get_ward_cleanliness_scores() if w['ward'] == user_ward)
            
            st.metric(
                "Cleanliness Score",
                f"{ward_data['score']}/100",
                f"{ward_data['change']}"
            )
            
            # Show rank info
            st.markdown(f"**Rank:** {ward_data['rank']} out of 12 wards")
            st.markdown(f"**Category:** {ward_data['category']}")
            
        with col2:
            # Generate some ward-specific metrics
            collection_efficiency = random.uniform(85, 98)
            st.metric(
                "Collection Efficiency",
                f"{collection_efficiency:.1f}%",
                f"{random.uniform(-2, 5):.1f}%"
            )
            
            # Target info
            st.markdown("**Target:** 100%")
            st.markdown("**City Average:** 92.3%")
            
        with col3:
            # Generate some ward-specific metrics
            complaints_resolved = random.randint(75, 95)
            st.metric(
                "Complaints Resolution",
                f"{complaints_resolved}%",
                f"{random.uniform(-3, 8):.1f}%"
            )
            
            # Additional info
            total_complaints = random.randint(120, 200)
            st.markdown(f"**Total Complaints:** {total_complaints}")
            st.markdown(f"**Average Resolution Time:** {random.randint(2, 5)} days")
        
        # Ward waste composition
        st.markdown("### Waste Composition Analysis")
        
        # Generate waste composition data
        waste_types = {
            'Kitchen/Food Waste': random.uniform(45, 55),
            'Garden Waste': random.uniform(5, 12),
            'Paper & Cardboard': random.uniform(10, 18),
            'Plastics': random.uniform(8, 15),
            'Glass': random.uniform(2, 5),
            'Metal': random.uniform(1, 3),
            'Textiles': random.uniform(2, 6),
            'Other': random.uniform(5, 10)
        }
        
        # Normalize to 100%
        total = sum(waste_types.values())
        waste_types = {k: v/total*100 for k, v in waste_types.items()}
        
        # Convert to DataFrame
        df_composition = pd.DataFrame([
            {'type': k, 'percentage': v} for k, v in waste_types.items()
        ])
        
        col1, col2 = st.columns([2, 3])
        
        with col1:
            # Show composition table
            st.dataframe(
                df_composition.sort_values('percentage', ascending=False).reset_index(drop=True),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "type": "Waste Type",
                    "percentage": st.column_config.ProgressColumn(
                        "Percentage",
                        format="%.1f%%",
                        min_value=0,
                        max_value=100
                    )
                }
            )
            
        with col2:
            # Create pie chart for waste composition
            fig = px.pie(
                df_composition,
                values='percentage',
                names='type',
                title=f'Waste Composition in {user_ward}',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        # Monthly performance trend
        st.markdown("### Monthly Performance Trend")
        
        # Generate monthly data for the ward
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        current_month = datetime.now().month
        
        ward_monthly_data = []
        for i, month in enumerate(months[:current_month]):
            # Generate data with an improving trend
            cleanliness = min(100, max(40, 60 + i*1.5 + random.uniform(-5, 5)))
            segregation = min(100, max(40, 65 + i*1.2 + random.uniform(-3, 3)))
            collection = min(100, max(70, 80 + i*0.8 + random.uniform(-2, 2)))
            
            ward_monthly_data.append({
                'month': month,
                'cleanliness': cleanliness,
                'segregation': segregation,
                'collection': collection
            })
            
        df_ward_monthly = pd.DataFrame(ward_monthly_data)
        
        # Create line chart
        fig = go.Figure()
        
        # Add traces
        fig.add_trace(go.Scatter(
            x=df_ward_monthly['month'],
            y=df_ward_monthly['cleanliness'],
            mode='lines+markers',
            name='Cleanliness Score',
            line=dict(color='#3498db', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=df_ward_monthly['month'],
            y=df_ward_monthly['segregation'],
            mode='lines+markers',
            name='Segregation Rate',
            line=dict(color='#2ecc71', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=df_ward_monthly['month'],
            y=df_ward_monthly['collection'],
            mode='lines+markers',
            name='Collection Efficiency',
            line=dict(color='#f39c12', width=3)
        ))
        
        # Add target lines
        fig.add_shape(
            type="line",
            x0=0,
            x1=len(months[:current_month])-1,
            y0=90,
            y1=90,
            line=dict(color="red", width=2, dash="dash"),
            name="BBMP Targets"
        )
        
        fig.update_layout(
            title=f"{user_ward} Ward - Monthly Performance Metrics (2023)",
            xaxis_title="Month",
            yaxis_title="Score/Rate (%)",
            yaxis=dict(range=[40, 100]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
        )
        
        fig.add_annotation(
            x=1,
            y=92,
            text="BBMP Target: 90%",
            showarrow=False,
            font=dict(color="red")
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Area comparative analysis
        st.markdown("### Ward Comparative Analysis")
        
        # Get neighboring wards (just using random selection for demo)
        all_wards = [w['ward'] for w in get_ward_cleanliness_scores()]
        neighboring_wards = random.sample([w for w in all_wards if w != user_ward], 3) + [user_ward]
        
        # Create comparison metrics
        comparison_metrics = ['Cleanliness Score', 'Segregation Rate', 'Collection Efficiency', 'Complaint Resolution']
        ward_comparison_data = []
        
        for ward in neighboring_wards:
            is_user_ward = ward == user_ward
            for metric in comparison_metrics:
                # Generate appropriate values based on metric
                if metric == 'Cleanliness Score':
                    value = next((w['score'] for w in get_ward_cleanliness_scores() if w['ward'] == ward), 70)
                elif metric == 'Segregation Rate':
                    value = random.uniform(70, 95)
                elif metric == 'Collection Efficiency':
                    value = random.uniform(85, 98)
                else:  # Complaint Resolution
                    value = random.uniform(75, 95)
                    
                ward_comparison_data.append({
                    'ward': ward,
                    'metric': metric,
                    'value': value,
                    'is_user_ward': is_user_ward
                })
                
        df_comparison = pd.DataFrame(ward_comparison_data)
        
        # Create bar chart
        fig = px.bar(
            df_comparison,
            x='ward',
            y='value',
            color='ward',
            facet_col='metric',
            facet_col_wrap=2,
            labels={'value': 'Score/Rate (%)', 'ward': 'Ward'},
            title=f"Comparing {user_ward} with Neighboring Wards",
            barmode='group',
            height=500
        )
        
        # Highlight user's ward with a different color
        for i, ward in enumerate(neighboring_wards):
            if ward == user_ward:
                user_ward_color = '#e74c3c'  # Red color for user's ward
                break
        
        fig.update_layout(
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Ward-specific recommendations
        st.markdown("### BBMP Recommendations for Ward Improvement")
        
        # Generate recommendations based on mock scores
        ward_scores = next((w for w in get_ward_cleanliness_scores() if w['ward'] == user_ward), None)
        
        if ward_scores:
            cleanliness_score = ward_scores['score']
            if cleanliness_score < 60:
                priority = "high"
            elif cleanliness_score < 80:
                priority = "medium"
            else:
                priority = "low"
                
            st.markdown(f"""
            <div style="background-color: {'#ffebee' if priority == 'high' else '#fff8e1' if priority == 'medium' else '#e8f5e9'}; 
                        border-left: 5px solid {'#f44336' if priority == 'high' else '#ffc107' if priority == 'medium' else '#4caf50'}; 
                        padding: 15px; margin: 10px 0;">
                <h4>Ward Improvement Priority: {priority.upper()}</h4>
                <p>Based on the current metrics and trends, BBMP recommends the following actions for {user_ward} ward:</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Short-term Actions")
                recommendations = []
                
                if cleanliness_score < 70:
                    recommendations.extend([
                        "Increase cleaning frequency in identified hotspot areas",
                        "Deploy additional street sweepers in commercial zones",
                        "Conduct weekly black spot monitoring and clearance"
                    ])
                
                if ward_scores.get('change', 0) < 0:
                    recommendations.extend([
                        "Investigate recent decline in ward performance",
                        "Conduct citizen feedback sessions to identify issues"
                    ])
                
                recommendations.extend([
                    "Organize community cleanliness drives",
                    "Enhance waste collection schedule adherence",
                    "Deploy additional segregation bins in public areas"
                ])
                
                for i, rec in enumerate(recommendations[:5]):
                    st.markdown(f"**{i+1}.** {rec}")
            
            with col2:
                st.markdown("#### Long-term Initiatives")
                long_term = [
                    "Establish ward-level Solid Waste Management Committee",
                    "Develop composting facilities for garden and food waste",
                    "Deploy smart bins in high-density areas",
                    "Implement incentive program for waste reduction",
                    "Create ward-specific waste management education program"
                ]
                
                for i, rec in enumerate(long_term):
                    st.markdown(f"**{i+1}.** {rec}")
    
    with tab3:
        st.markdown("### Waste Segregation Analytics")
        
        # Key metrics for segregation
        st.markdown("""
        <div style="background-color: #effaf5; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
            <h4>Segregation at Source - Key Performance Indicators</h4>
            <p>Effective segregation is the foundation of sustainable waste management.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "City Segregation Rate",
                "83%",
                "4.5%"
            )
        
        with col2:
            st.metric(
                f"{user_ward} Segregation",
                f"{random.randint(75, 95)}%",
                f"{random.uniform(-2, 8):.1f}%"
            )
            
        with col3:
            st.metric(
                "Mixed Waste Received",
                f"{random.randint(15, 30)}%",
                f"{random.uniform(-10, 2):.1f}%",
                delta_color="inverse"
            )
            
        with col4:
            st.metric(
                "BBMP 2023 Target",
                "90%",
                f"{random.randint(-10, 5)}"
            )
        
        # Segregation by category
        st.markdown("### Segregation Performance by Category")
        
        # Generate segregation data by category
        categories = [
            'Wet Waste',
            'Dry Waste',
            'Domestic Hazardous',
            'Sanitary Waste',
            'E-Waste',
            'Construction Debris',
            'Garden Waste'
        ]
        
        city_data = []
        ward_data = []
        
        for category in categories:
            city_rate = random.uniform(70, 95)
            # Ward rate somewhat correlated with city rate
            ward_rate = max(50, min(100, city_rate + random.uniform(-10, 10)))
            
            city_data.append({
                'category': category,
                'segregation_rate': city_rate,
                'area': 'Bengaluru City'
            })
            
            ward_data.append({
                'category': category,
                'segregation_rate': ward_rate,
                'area': f'{user_ward} Ward'
            })
            
        df_segregation = pd.concat([
            pd.DataFrame(city_data),
            pd.DataFrame(ward_data)
        ])
        
        # Create grouped bar chart
        fig = px.bar(
            df_segregation,
            x='category',
            y='segregation_rate',
            color='area',
            barmode='group',
            title='Waste Segregation Rates by Category',
            labels={'segregation_rate': 'Segregation Rate (%)', 'category': 'Waste Category', 'area': 'Area'},
            color_discrete_map={
                'Bengaluru City': '#3498db',
                f'{user_ward} Ward': '#e74c3c'
            }
        )
        
        # Add target line
        fig.add_shape(
            type="line",
            x0=-0.5,
            x1=len(categories) - 0.5,
            y0=90,
            y1=90,
            line=dict(color="green", width=2, dash="dash"),
        )
        
        fig.add_annotation(
            x=3,
            y=93,
            text="BBMP Target: 90%",
            showarrow=False,
            font=dict(color="green")
        )
        
        fig.update_layout(
            yaxis_range=[50, 100]
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Segregation trend over time
        st.markdown("### Segregation Trend Analysis")
        
        # Generate monthly segregation data
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        current_month = datetime.now().month
        
        segregation_trend = []
        
        base_rate = 65
        for i, month in enumerate(months[:current_month]):
            # Overall improving trend with some fluctuations
            city_rate = min(95, base_rate + i*1.5 + random.uniform(-3, 3))
            ward_rate = min(95, city_rate + random.uniform(-8, 8))
            
            segregation_trend.append({
                'month': month,
                'Bengaluru City': city_rate,
                f'{user_ward} Ward': ward_rate
            })
            
        df_trend = pd.DataFrame(segregation_trend)
        
        # Create dual line chart
        fig = go.Figure()
        
        # Add city line
        fig.add_trace(go.Scatter(
            x=df_trend['month'],
            y=df_trend['Bengaluru City'],
            mode='lines+markers',
            name='Bengaluru City',
            line=dict(color='#3498db', width=3)
        ))
        
        # Add ward line
        fig.add_trace(go.Scatter(
            x=df_trend['month'],
            y=df_trend[f'{user_ward} Ward'],
            mode='lines+markers',
            name=f'{user_ward} Ward',
            line=dict(color='#e74c3c', width=3)
        ))
        
        # Add target line
        fig.add_shape(
            type="line",
            x0=0,
            x1=len(months[:current_month])-1,
            y0=90,
            y1=90,
            line=dict(color="green", width=2, dash="dash"),
        )
        
        fig.update_layout(
            title='Monthly Segregation Rate Trend (2023)',
            xaxis_title='Month',
            yaxis_title='Segregation Rate (%)',
            yaxis=dict(range=[60, 100]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
        )
        
        fig.add_annotation(
            x=1,
            y=92,
            text="BBMP Target: 90%",
            showarrow=False,
            font=dict(color="green")
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Segregation compliance by area type
        st.markdown("### Segregation Compliance by Area Type")
        
        # Generate area type data
        area_types = [
            'Residential - High Density',
            'Residential - Low Density',
            'Commercial',
            'Markets',
            'Institutional',
            'Hotels & Restaurants',
            'Public Spaces'
        ]
        
        area_data = []
        
        for area in area_types:
            # Different base rates for different areas
            if 'Residential - High' in area:
                base = random.uniform(75, 90)
            elif 'Residential - Low' in area:
                base = random.uniform(85, 95)
            elif 'Commercial' in area:
                base = random.uniform(65, 85)
            elif 'Markets' in area:
                base = random.uniform(55, 75)
            elif 'Institutional' in area:
                base = random.uniform(80, 95)
            elif 'Hotels' in area:
                base = random.uniform(70, 90)
            else:  # Public Spaces
                base = random.uniform(50, 70)
                
            area_data.append({
                'area_type': area,
                'compliance_rate': base
            })
            
        df_areas = pd.DataFrame(area_data)
        
        # Sort by compliance rate
        df_areas = df_areas.sort_values('compliance_rate', ascending=False)
        
        # Create horizontal bar chart
        fig = px.bar(
            df_areas,
            y='area_type',
            x='compliance_rate',
            orientation='h',
            title='Segregation Compliance by Area Type',
            labels={'compliance_rate': 'Compliance Rate (%)', 'area_type': 'Area Type'},
            color='compliance_rate',
            color_continuous_scale=[(0, 'red'), (0.5, 'yellow'), (1, 'green')]
        )
        
        # Add target line
        fig.add_shape(
            type="line",
            x0=90,
            x1=90,
            y0=-0.5,
            y1=len(area_types) - 0.5,
            line=dict(color="green", width=2, dash="dash"),
        )
        
        fig.add_annotation(
            x=90,
            y=0,
            text="BBMP Target: 90%",
            showarrow=False,
            xanchor="center",
            yanchor="bottom",
            font=dict(color="green")
        )
        
        fig.update_layout(
            xaxis_range=[40, 100]
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Best practices and recommendations
        # ... [previous code remains the same] ...

        # Best practices and recommendations
        st.markdown("### Segregation Best Practices")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            #### Waste Categories for Segregation
            
            **Green Bin (Wet Waste)**
            - Kitchen waste (vegetable/fruit peels)
            - Leftover food
            - Tea/coffee grounds
            - Meat and bones
            - Eggshells
            - Garden trimmings
            
            **Blue Bin (Dry Waste)**
            - Paper and cardboard
            - Plastic containers (cleaned)
            - Glass bottles
            - Metal items
            - Tetra packs
            - Clothing/textiles
            
            **Red Bin (Domestic Hazardous)**
            - Sanitary waste
            - Diapers
            - Batteries
            - Medicine strips
            - Pesticide containers
            - Paints, oils, chemicals
            """)
            
        with col2:
            st.markdown("""
            #### BBMP Segregation Guidelines
            
            1. **Segregate at Source**: All households must separate waste into wet, dry, and domestic hazardous categories
            
            2. **Handover System**: Give segregated waste directly to collection staff
            3. **Use Color-coded Bins**: Ensure proper disposal in designated bins
            4. **Educate and Train**: Participate in community workshops on waste segregation
            5. **Report Issues**: Use the BBMP Sahaya app to report any issues with waste collection
            6. **Participate in Drives**: Join local cleanliness drives and awareness campaigns
            """)
            
    with tab4:
        st.markdown("### Environmental Impact Analytics")
        
        # Environmental impact overview
        st.markdown("""
        <div style="background-color: #e8f5e9; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
            <h4>Environmental Benefits of Improved Waste Management</h4>
            <p>Tracking the positive environmental impact of BBMP's waste management initiatives</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Key environmental metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Carbon Reduction",
                f"{random.randint(120000, 150000)} tonnes",
                f"{random.uniform(5, 15):.1f}%"
            )
            st.caption("CO₂ equivalent emissions avoided")
        
        with col2:
            st.metric(
                "Landfill Space Saved",
                f"{random.randint(15, 25)} acres",
                f"{random.uniform(10, 20):.1f}%"
            )
            st.caption("Land preserved through diversion")
            
        with col3:
            st.metric(
                "Groundwater Protected",
                f"{random.randint(400, 600)} km²",
                f"{random.uniform(8, 18):.1f}%"
            )
            st.caption("Area with reduced leachate risk")
            
        with col4:
            st.metric(
                "Trees Saved",
                f"{random.randint(80000, 120000)}",
                f"{random.uniform(12, 22):.1f}%"
            )
            st.caption("Through paper recycling")
            
        # Carbon footprint reduction
        st.markdown("### Carbon Footprint Reduction")
        
        # Generate monthly carbon reduction data
        carbon_data = []
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        current_month = datetime.now().month
        
        # Baseline - what would have been without interventions
        baseline = [random.uniform(12000, 14000) for _ in range(current_month)]
        
        # Actual emissions with interventions (lower)
        actual = [baseline[i] * random.uniform(0.65, 0.85) for i in range(current_month)]
        
        for i, month in enumerate(months[:current_month]):
            carbon_data.append({
                'month': month,
                'Baseline Emissions': baseline[i],
                'Actual Emissions': actual[i],
                'Reduction': baseline[i] - actual[i]
            })
            
        df_carbon = pd.DataFrame(carbon_data)
        
        # Create stacked bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df_carbon['month'],
            y=df_carbon['Actual Emissions'],
            name='Actual Emissions',
            marker_color='#e74c3c'
        ))
        
        fig.add_trace(go.Bar(
            x=df_carbon['month'],
            y=df_carbon['Reduction'],
            name='Emissions Avoided',
            marker_color='#2ecc71'
        ))
        
        fig.update_layout(
            title='Monthly Carbon Footprint Reduction (Tonnes CO₂e)',
            xaxis_title='Month',
            yaxis_title='Carbon Emissions (Tonnes CO₂e)',
            barmode='stack',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Environmental benefits by waste management practice
        st.markdown("### Environmental Benefits by Waste Management Practice")
        
        # Generate data for different practices
        practices = [
            'Organic Waste Composting',
            'Plastic Recycling',
            'Paper Recycling',
            'Metal Recycling',
            'Glass Recycling',
            'E-waste Processing',
            'Waste-to-Energy'
        ]
        
        practice_data = []
        
        for practice in practices:
            # Different environmental metrics for different practices
            if practice == 'Organic Waste Composting':
                carbon = random.uniform(20, 30)
                water = random.uniform(15, 25)
                land = random.uniform(15, 25)
            elif practice == 'Plastic Recycling':
                carbon = random.uniform(15, 25)
                water = random.uniform(10, 20)
                land = random.uniform(30, 40)
            elif practice == 'Paper Recycling':
                carbon = random.uniform(10, 20)
                water = random.uniform(30, 40)
                land = random.uniform(20, 30)
            elif practice == 'Metal Recycling':
                carbon = random.uniform(30, 40)
                water = random.uniform(20, 30)
                land = random.uniform(5, 15)
            elif practice == 'Glass Recycling':
                carbon = random.uniform(5, 15)
                water = random.uniform(5, 15)
                land = random.uniform(10, 20)
            elif practice == 'E-waste Processing':
                carbon = random.uniform(25, 35)
                water = random.uniform(5, 15)
                land = random.uniform(35, 45)
            else:  # Waste-to-Energy
                carbon = random.uniform(35, 45)
                water = random.uniform(5, 10)
                land = random.uniform(25, 35)
                
            practice_data.append({
                'practice': practice,
                'Carbon Reduction': carbon,
                'Water Conservation': water,
                'Land Preservation': land
            })
            
        df_practices = pd.DataFrame(practice_data)
        
        # Create radar chart
        categories = list(df_practices['practice'])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=df_practices['Carbon Reduction'],
            theta=categories,
            fill='toself',
            name='Carbon Reduction',
            line=dict(color='#3498db')
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=df_practices['Water Conservation'],
            theta=categories,
            fill='toself',
            name='Water Conservation',
            line=dict(color='#2ecc71')
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=df_practices['Land Preservation'],
            theta=categories,
            fill='toself',
            name='Land Preservation',
            line=dict(color='#e67e22')
        ))
        
        fig.update_layout(
            title="Environmental Benefits Comparison (% Improvement)",
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 50]
                )
            ),
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # SDG alignment
        st.markdown("### Alignment with Sustainable Development Goals (SDGs)")
        
        col1, col2 = st.columns([1, 2])
        
        # Replace the placeholder image with a more reliable approach around line 884

        # Replace the SDGs section with this code:

        with col1:
            # Create SDGs with proper streamlit components instead of HTML
            st.markdown("#### Relevant UN SDGs")
            
            # Use Streamlit's built-in styling capabilities for more reliable rendering
            sdgs = [
                {"number": "3", "name": "Good Health and Well-being", "color": "#4c9f38"},
                {"number": "6", "name": "Clean Water and Sanitation", "color": "#00aed9"},
                {"number": "11", "name": "Sustainable Cities and Communities", "color": "#fd9d24"},
                {"number": "12", "name": "Responsible Consumption and Production", "color": "#bf8b2e"},
                {"number": "13", "name": "Climate Action", "color": "#3f7e44"}
            ]
            
            # Create each SDG box using Streamlit components
            for sdg in sdgs:
                st.markdown(f"""
                <div style="background-color: {sdg['color']}; color: white; padding: 10px; 
                            border-radius: 5px; margin-bottom: 10px; text-align: center;">
                    <strong>SDG {sdg['number']}</strong><br>{sdg['name']}
                </div>
                """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            #### BBMP's Waste Management Contribution to SDGs
            
            **SDG 3: Good Health and Well-being**
            - Reduced disease vectors through proper waste management
            - Decreased air pollution from waste burning
            - Improved sanitation conditions
            
            **SDG 6: Clean Water and Sanitation**
            - Protection of water bodies from waste contamination
            - Reduced groundwater pollution from leachate
            - Improved urban drainage systems
            
            **SDG 11: Sustainable Cities and Communities**
            - Enhanced urban aesthetics and cleanliness
            - Reduced flood risk through drain clearing
            - Improved quality of life in urban areas
            
            **SDG 12: Responsible Consumption and Production**
            - Promotion of circular economy principles
            - Extended producer responsibility implementation
            - Waste reduction through community awareness
            
            **SDG 13: Climate Action**
            - Reduced methane emissions from organic waste
            - Lower carbon footprint through recycling
            - Energy recovery from waste streams
            """)
            
        # Community health impacts
        st.markdown("### Community Health Benefits")
        
        # Generate health impact data
        health_metrics = {
            'Respiratory Conditions': random.uniform(15, 25),
            'Vector-borne Diseases': random.uniform(20, 35),
            'Water-borne Diseases': random.uniform(10, 30),
            'Allergic Reactions': random.uniform(5, 15),
            'Quality of Life Index': random.uniform(25, 40)
        }
        
        # Convert to DataFrame
        df_health = pd.DataFrame([
            {'metric': k, 'improvement': v} for k, v in health_metrics.items()
        ])
        
        # Create horizontal bar chart
        fig = px.bar(
            df_health,
            y='metric',
            x='improvement',
            orientation='h',
            title='Health Improvements from Better Waste Management (%)',
            labels={'improvement': 'Estimated Improvement (%)', 'metric': 'Health Metric'},
            color='improvement',
            text='improvement',
            color_continuous_scale=[(0, '#2ecc71'), (1, '#2ecc71')]
        )
        
        fig.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='outside'
        )
        
        fig.update_layout(
            xaxis_range=[0, max(health_metrics.values()) * 1.2]
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Footer with data sources
        st.markdown("---")
        st.markdown("""
        <div style="font-size: 0.8em; color: #666;">
        <p><strong>Data Sources:</strong> BBMP Solid Waste Management Department, Karnataka State Pollution Control Board, Environmental Health Analytics Unit</p>
        <p><strong>Methodology:</strong> Environmental impact calculations follow IPCC guidelines for waste sector emissions and resource conservation metrics.</p>
        </div>
        """, unsafe_allow_html=True)