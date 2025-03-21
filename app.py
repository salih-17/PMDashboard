import streamlit as st
import pandas as pd
from data import load_project_data, load_summary_data
from components import (
    display_sidebar_filters, 
    display_summary_cards, 
    display_project_table,
    display_project_counts
)
from utils import apply_filters

# Page configuration
st.set_page_config(
    page_title="Projects Overview",
    page_icon="📊",
    layout="wide",
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Global styles */
    .main {
        padding-top: 0;
        background-color: #f7f9fc;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0;
        max-width: 1300px;
    }
    
    /* Streamlit element adjustments */
    .stProgress > div > div > div {
        height: 15px;
    }
    div[data-testid="stSidebarUserContent"] {
        padding-top: 1.5rem;
        background-color: #0A2463;
        color: white;
    }
    div[data-testid="stSidebar"] {
        background-color: #0A2463;
    }
    section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] div[data-baseweb="select"] div {
        color: white !important;
    }
    button[kind="primaryFormSubmit"] {
        background-color: #1E5AF5 !important;
        border-radius: 4px !important;
    }
    
    /* Status badges */
    .status-badge {
        border-radius: 20px;
        padding: 0.25rem 0.7rem;
        color: white;
        font-size: 0.8rem;
        font-weight: 500;
        display: inline-block;
        min-width: 80px;
        text-align: center;
    }
    .ongoing-red {
        background-color: #FF5252;
    }
    .ongoing-orange {
        background-color: #FFA726;
    }
    .ongoing-green {
        background-color: #66BB6A;
    }
    .closed {
        background-color: #212121;
    }
    
    /* Progress elements */
    .progress-text {
        position: absolute;
        right: 10px;
        font-size: 0.8rem;
        color: #0A2463;
        font-weight: 500;
    }
    
    /* Header and title elements */
    .dashboard-header {
        background: linear-gradient(90deg, #0A2463 0%, #1E5AF5 100%);
        color: white;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 12px rgba(10, 36, 99, 0.15);
    }
    .dashboard-title {
        font-size: 24px;
        font-weight: 600;
        margin: 0;
    }
    .dashboard-subtitle {
        font-size: 14px;
        opacity: 0.8;
        margin: 5px 0 0 0;
    }
    .header-right {
        display: flex;
        align-items: center;
    }
    .date-display {
        background: rgba(255, 255, 255, 0.2);
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 14px;
        display: flex;
        align-items: center;
    }
    
    /* Sidebar elements */
    .sidebar-icon {
        font-size: 1.5rem;
        color: white;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    .sidebar-title {
        text-align: center;
        color: white;
        margin-bottom: 1.5rem;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Metric cards */
    .metric-card {
        background-color: white;
        padding: 1.2rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: bold;
        color: #0A2463;
        margin: 10px 0;
        line-height: 1;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 5px;
    }
    .metric-icon {
        font-size: 2.2rem;
        color: #1E5AF5;
        margin-bottom: 5px;
    }
    
    /* Avatar and user elements */
    .avatar-img {
        border-radius: 50%;
        width: 32px;
        height: 32px;
        margin-right: 10px;
        background-color: #e5e9f2;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: #0A2463;
    }
    .avatar-container {
        display: flex;
        align-items: center;
    }
    
    /* Project table elements */
    .project-row {
        padding: 12px 0;
        border-bottom: 1px solid #eee;
        transition: background-color 0.15s ease;
        align-items: center;
    }
    .project-row:hover {
        background-color: #f5f8ff;
    }
    .time-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
        font-weight: bold;
        color: white;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .time-green {
        background-color: #66BB6A;
    }
    .time-orange {
        background-color: #FFA726;
    }
    .time-red {
        background-color: #FF5252;
    }
    
    /* Table layout */
    .projects-table {
        margin-top: 1.5rem;
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    .table-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    .column-headers {
        font-weight: 600;
        border-bottom: 2px solid #eaeef2;
        padding-bottom: 12px;
        color: #0A2463;
    }
    .projects-overview-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #0A2463;
        margin: 0;
    }
    
    /* Legend and color definitions */
    .color-definition-container {
        background-color: white;
        padding: 10px 15px;
        border-radius: 8px;
        margin: 15px 0;
        font-size: 0.85rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    .color-definition-title {
        font-weight: 600;
        margin-bottom: 5px;
        color: #0A2463;
    }
    .color-definition {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
    }
    .color-item {
        display: flex;
        align-items: center;
    }
    .color-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 6px;
    }
    .red-text, .red-dot {
        color: #FF5252;
        background-color: #FF5252;
    }
    .orange-text, .orange-dot {
        color: #FFA726;
        background-color: #FFA726;
    }
    .green-text, .green-dot {
        color: #66BB6A;
        background-color: #66BB6A;
    }
    .black-text, .black-dot {
        color: #212121;
        background-color: #212121;
    }
    
    /* Count cards */
    .count-card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 15px;
        transition: transform 0.2s ease;
    }
    .count-card:hover {
        transform: translateY(-3px);
    }
    .count-value {
        font-size: 2rem;
        font-weight: bold;
        color: #0A2463;
        margin: 5px 0;
    }
    .count-label {
        font-size: 0.9rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Create layout with sidebar and main content
with st.container():
    # Modern dashboard header with date and overview
    from datetime import datetime
    today = datetime.now().strftime("%B %d, %Y")
    
    st.markdown(f"""
    <div class="dashboard-header">
        <div>
            <h1 class="dashboard-title">Projects Dashboard</h1>
            <p class="dashboard-subtitle">Comprehensive overview of all project activities and metrics</p>
        </div>
        <div class="header-right">
            <div class="date-display">
                <span style="margin-right: 8px;">📅</span> {today}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction text
    st.markdown("""
    <div style="background-color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);">
        <div style="display: flex; align-items: flex-start;">
            <div style="font-size: 2rem; margin-right: 15px; color: #1E5AF5;">📌</div>
            <div>
                <div style="font-weight: 600; font-size: 1.1rem; margin-bottom: 8px; color: #0A2463;">Welcome to the Project Management Dashboard</div>
                <p style="margin: 0 0 8px 0; color: #444; font-size: 0.95rem;">
                    This interactive dashboard provides a comprehensive overview of all projects, 
                    helping you track budgets, timelines, and progress in real-time. Use the filters
                    on the left to narrow down specific projects or view by status.
                </p>
                <p style="margin: 0; color: #444; font-size: 0.95rem;">
                    The color-coding system helps identify projects that need attention based on their
                    remaining time and completion status.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    projects_df = load_project_data()
    summary_data = load_summary_data()
    
    # Apply sidebar filters
    filter_params = display_sidebar_filters(projects_df)
    
    # Apply filters to the dataframe
    filtered_df = apply_filters(projects_df, filter_params)
    
    # Display project counts with filtered data
    display_project_counts(filtered_df)
    
    # Summary cards at the top
    display_summary_cards(summary_data)
    
    # Display projects table with filtered data (expanded to full width)
    display_project_table(filtered_df)
