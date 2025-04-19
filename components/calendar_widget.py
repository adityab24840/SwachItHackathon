# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar

def generate_disposal_history(user_id, days=30):
    """
    Generate or fetch user's waste disposal history
    In a real app, this would query a database
    """
    # Seed with user_id to get consistent but unique results
    np.random.seed(hash(user_id) % 2**32)
    
    # Get current date and go back 'days' days
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    # Generate all dates in range
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    
    # Generate random disposal statuses (True/False) with higher probability on weekdays
    # and occasional missing days (None)
    disposals = []
    for date in date_range:
        if date.weekday() < 5:  # Weekday (Monday=0, Sunday=6)
            status = np.random.choice([True, False, None], p=[0.7, 0.2, 0.1])
        else:  # Weekend
            status = np.random.choice([True, False, None], p=[0.3, 0.6, 0.1])
        disposals.append(status)
    
    # Create DataFrame - explicitly convert to datetime type
    history = pd.DataFrame({
        'date': pd.to_datetime(date_range),  # Convert to pandas datetime
        'disposed': disposals
    })
    
    return history

def render_calendar_widget(user_id):
    """Render calendar showing waste disposal history"""
    st.write("Track your waste disposal habits to earn maximum rewards")
    
    # Get user's disposal history
    history = generate_disposal_history(user_id)
    
    # Create monthly calendar view
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Allow user to select month to view
    months = list(calendar.month_name)[1:]
    selected_month_name = st.selectbox(
        "Select Month", 
        months, 
        index=current_month-1,
        key="calendar_month_selector"
    )
    selected_month = months.index(selected_month_name) + 1
    
    # Get number of days in the selected month
    days_in_month = calendar.monthrange(current_year, selected_month)[1]
    
    # Extract data for the selected month
    month_history = history[
        (history['date'].dt.month == selected_month) & 
        (history['date'].dt.year == current_year)
    ]
    
    # Map dates to their disposal status
    date_status_map = dict(zip(month_history['date'].dt.day, month_history['disposed']))
    
    # Display day names as headers
    cols = st.columns(7)
    for i, day_name in enumerate(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']):
        cols[i].write(f"**{day_name}**")
    
    # Get the first day of the month (0 = Monday, 6 = Sunday)
    first_day = calendar.monthrange(current_year, selected_month)[0]
    
    # Create calendar grid
    day_counter = 1
    
    # Create 6 rows max (some months need 6 rows)
    for week in range(6):
        cols = st.columns(7)
        
        for weekday in range(7):
            # Skip days before the first day of month
            if week == 0 and weekday < first_day:
                cols[weekday].write("")
                continue
            
            # Stop after last day of month
            if day_counter > days_in_month:
                break
                
            # Get disposal status for this day
            status = date_status_map.get(day_counter, None)
            
            # Set cell style based on disposal status
            if status == True:
                cell_style = "background-color: #a8e6cf; border-radius: 5px; padding: 10px; text-align: center;"
                icon = "✅"
            elif status == False:
                cell_style = "background-color: #ff8b94; border-radius: 5px; padding: 10px; text-align: center;"
                icon = "❌"
            else:
                cell_style = "background-color: #f1f1f1; border-radius: 5px; padding: 10px; text-align: center;"
                icon = "—"
            
            # Write day number with appropriate style
            cols[weekday].markdown(f"""
            <div style="{cell_style}">
                <span>{day_counter}</span><br>
                <span>{icon}</span>
            </div>
            """, unsafe_allow_html=True)
            
            day_counter += 1
        
        # If we've displayed all days, break out of the outer loop
        if day_counter > days_in_month:
            break
    
    # Show legend
    st.write("")
    col1, col2, col3 = st.columns(3)
    col1.markdown('<span style="background-color: #a8e6cf; padding: 5px 10px; border-radius: 3px;">✅ Waste disposed properly</span>', unsafe_allow_html=True)
    col2.markdown('<span style="background-color: #ff8b94; padding: 5px 10px; border-radius: 3px;">❌ Missed disposal</span>', unsafe_allow_html=True)
    col3.markdown('<span style="background-color: #f1f1f1; padding: 5px 10px; border-radius: 3px;">— No data available</span>', unsafe_allow_html=True)

    # Show statistics
    st.write("")
    st.write("#### Monthly Statistics")
    
    # Calculate statistics - handle case where month_history may be empty
    total_days = len(month_history)
    if total_days > 0:
        # Make calculations
        total_disposed = month_history['disposed'].sum()
        total_missed = month_history['disposed'].isna().sum() + (total_days - total_disposed)
        total_percentage = (total_disposed / total_days) * 100
    else:
        total_disposed = 0
        total_missed = 0
        total_percentage = 0
    # Display statistics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Days", total_days)
    col2.metric("Total Disposed", total_disposed)
    col3.metric("Total Missed", total_missed)
    col4, col5 = st.columns(2)
    col4.metric("Disposal Rate", f"{total_percentage:.2f}%", delta_color="normal")
    col5.metric("Missed Rate", f"{100 - total_percentage:.2f}%", delta_color="inverse")
    # Show tips for improvement
    st.write("")
    st.write("#### Tips for Improvement")
    st.write("1. Set reminders for waste disposal days.")
    st.write("2. Use separate bins for dry and wet waste.")
    st.write("3. Participate in community clean-up drives.")
    