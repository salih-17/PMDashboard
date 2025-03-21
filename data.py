import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

@st.cache_data
def load_project_data():
    """
    Load project data with the same structure as shown in the image
    """
    # Create sample data based on the image
    data = {
        'project_manager': [
            'Abdurrahman Salih', 
            'Abdurrahman Salih', 
            'Badr Al-Din Triyaki', 
            'Badr Al-Din Triyaki'
        ],
        'avatar': [
            'avatar1.svg', 
            'avatar1.svg', 
            'avatar2.svg', 
            'avatar2.svg'
        ],
        'project_name': ['OCHA', 'WFP', 'GIRO', 'USAID'],
        'status': ['Ongoing', 'Ongoing', 'Closed', 'Ongoing'],
        'budget': [250000, 750000, 50000, 180000],
        'remaining_time_pct': [11, 57, 0, 94],
        'start_date': ['10/1/2024', '11/1/2024', '10/1/2024', '1/15/2025'],
        'end_date': ['2/1/2025', '5/1/2025', '12/30/2024', '6/1/2025'],
        'progress_pct': [93, 80, 96, 10]
    }
    
    df = pd.DataFrame(data)
    
    # Calculate days remaining for status color determination
    df['start_date_dt'] = pd.to_datetime(df['start_date'])
    df['end_date_dt'] = pd.to_datetime(df['end_date'])
    
    # Calculate days remaining based on end date
    today = datetime.now()
    df['days_remaining'] = (df['end_date_dt'] - today).dt.days
    
    # Determine status color
    def determine_status_color(row):
        if row['status'] == 'Closed':
            return 'closed'
        elif row['days_remaining'] < 60:
            return 'ongoing-red'
        elif row['days_remaining'] < 120:
            return 'ongoing-orange'
        else:
            return 'ongoing-green'
    
    df['status_color'] = df.apply(determine_status_color, axis=1)
    
    return df

@st.cache_data
def load_summary_data():
    """
    Load summary metrics data
    """
    summary = {
        'total_budget': 1230000,  # $1.23M
        'projects_count': 4,
        'households_reached': 698,
        'individuals_reached': 3490
    }
    
    return summary
