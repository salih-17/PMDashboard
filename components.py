import streamlit as st
import pandas as pd
from datetime import datetime

def display_sidebar_filters(df):
    """Display sidebar filters and return the selected filter values"""
    
    # Sidebar header with logo and title
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <div style="font-size: 2.2rem; margin-bottom: 0.5rem; color: white;">📊</div>
        <div style="font-size: 1.3rem; font-weight: 600; color: white; margin-bottom: 0.2rem;">Projects Tracker</div>
        <div style="font-size: 1.3rem; font-weight: 600; color: white; margin-bottom: 0.2rem;">Created by: Abdurrahman Salih</div>
        <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7); margin-bottom: 1rem;">Dashboard & Reporting Tool</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for filters if they don't exist
    if 'filters_initialized' not in st.session_state:
        st.session_state.filters_initialized = True
        st.session_state.manager_filter = 'All'
        st.session_state.project_filter = 'All'  
        st.session_state.status_filter = 'All'
        st.session_state.timeline_filter = 'All'
    
    # Filter section header
    st.sidebar.markdown("""
    <div style="display: flex; align-items: center; margin: 1rem 0 1.5rem 0;">
        <div style="font-size: 1.1rem; font-weight: 600; color: white; display: flex; align-items: center;">
            <span style="margin-right: 8px;">🔍</span> Filter Projects
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Project manager filter with icon
    st.sidebar.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 0.3rem;">
        <span style="margin-right: 8px; color: rgba(0,0,0,0.8);">👤</span>
        <span style="color: rgba(0,0,0,0.8); font-weight: 500;">Project Manager</span>
    </div>
    """, unsafe_allow_html=True)
    
    all_managers = ['All'] + sorted(df['project_manager'].unique().tolist())
    manager_filter = st.sidebar.selectbox(
        "Select project manager", 
        options=all_managers, 
        key='manager_filter',
        label_visibility='collapsed'
    )
    
    # Apply manager filter to dataframe for cascading filters
    filtered_df = df.copy()
    if manager_filter != 'All':
        filtered_df = filtered_df[filtered_df['project_manager'] == manager_filter]
    
    # Project name filter with icon
    st.sidebar.markdown("""
    <div style="display: flex; align-items: center; margin: 1rem 0 0.3rem 0;">
        <span style="margin-right: 8px; color: rgba(255,255,255,0.8);">📋</span>
        <span style="color: rgba(0,0,0,0.8); font-weight: 500;">Project Name</span>
    </div>
    """, unsafe_allow_html=True)
    
    all_projects = ['All'] + sorted(filtered_df['project_name'].unique().tolist())
    project_filter = st.sidebar.selectbox(
        "Select project", 
        options=all_projects, 
        key='project_filter',
        label_visibility='collapsed'
    )
    
    # Apply project filter for cascading filters
    if project_filter != 'All':
        filtered_df = filtered_df[filtered_df['project_name'] == project_filter]
    
    # Status filter with icon
    st.sidebar.markdown("""
    <div style="display: flex; align-items: center; margin: 1rem 0 0.3rem 0;">
        <span style="margin-right: 8px; color: rgba(255,255,255,0.8);">🔄</span>
        <span style="color: rgba(0,0,0,0.8); font-weight: 500;">Status</span>
    </div>
    """, unsafe_allow_html=True)
    
    all_statuses = ['All'] + sorted(filtered_df['status'].unique().tolist())
    status_filter = st.sidebar.selectbox(
        "Select status", 
        options=all_statuses, 
        key='status_filter',
        label_visibility='collapsed'
    )
    
    # Timeline Flag filter with icon
    st.sidebar.markdown("""
    <div style="display: flex; align-items: center; margin: 1rem 0 0.3rem 0;">
        <span style="margin-right: 8px; color: rgba(255,255,255,0.8);">⏱️</span>
        <span style="color: rgba(0,0,0,0.8); font-weight: 500;">Timeline Flag</span>
    </div>
    """, unsafe_allow_html=True)
    
    timeline_filter = st.sidebar.selectbox(
        "Select timeline", 
        options=['All', 'Red', 'Orange', 'Green', 'Closed'], 
        key='timeline_filter',
        label_visibility='collapsed'
    )
    
    # Clear filters button with improved styling
    st.sidebar.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    if st.sidebar.button("Clear All Filters", use_container_width=True):
        st.session_state.manager_filter = 'All'
        st.session_state.project_filter = 'All'  
        st.session_state.status_filter = 'All'
        st.session_state.timeline_filter = 'All'
        st.rerun()
    
    # Show active filters
    active_filters = []
    if manager_filter != 'All':
        active_filters.append(f"Manager: {manager_filter}")
    if project_filter != 'All':
        active_filters.append(f"Project: {project_filter}")
    if status_filter != 'All':
        active_filters.append(f"Status: {status_filter}")
    if timeline_filter != 'All':
        active_filters.append(f"Timeline: {timeline_filter}")
    
    if active_filters:
        st.sidebar.markdown("<hr style='margin: 1.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
        st.sidebar.markdown("""
        <div style="color: white; font-weight: 500; margin-bottom: 0.5rem;">
            <span style="margin-right: 8px;">🏷️</span> Active Filters
        </div>
        """, unsafe_allow_html=True)
        
        for filter_text in active_filters:
            st.sidebar.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); padding: 8px 12px; border-radius: 4px; margin-bottom: 8px; font-size: 0.9rem; color: rgba(255,255,255,0.9);">
                {filter_text}
            </div>
            """, unsafe_allow_html=True)
    
    # Add footer information
    st.sidebar.markdown("<hr style='margin: 2rem 0 1rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
    st.sidebar.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.5); font-size: 0.8rem;">
        <div>Project Tracker v1.0</div>
        <div style="margin-top: 0.2rem;">Last updated: Mar 21, 2025</div>
    </div>
    """, unsafe_allow_html=True)
    
    return {
        'manager': manager_filter,
        'project': project_filter,
        'status': status_filter,
        'timeline': timeline_filter
    }

def display_project_counts(df=None):
    """Display donors and ongoing projects counts based on filtered data"""
    
    # If no dataframe is provided, use the default counts
    donors_count = 4
    ongoing_count = 3
    completed_count = 2
    critical_count = 1
    
    # If a dataframe is provided, count the actual number of donors and ongoing projects
    if df is not None:
        # Count unique project names as donors
        donors_count = df['project_name'].nunique()
        # Count ongoing projects
        ongoing_count = len(df[df['status'] == 'Ongoing'])
        # Count completed projects
        completed_count = len(df[df['status'] == 'Closed'])
        # Count critical projects (less than 60 days remaining and status is not Closed)
        critical_count = len(df[(df['status'] != 'Closed') & (df['days_remaining'] < 60)])
    
    # Add section header
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin: 20px 0 15px 0;">
        <h3 style="margin: 0; color: #0A2463; font-size: 1.2rem;">Project Overview</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a 4-column layout for the count cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="count-card">
            <div style="font-size: 2rem; color: #1E5AF5; margin-bottom: 5px;">🏛️</div>
            <div class="count-value">{donors_count}</div>
            <div class="count-label">Donors</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="count-card">
            <div style="font-size: 2rem; color: #1E5AF5; margin-bottom: 5px;">⚙️</div>
            <div class="count-value">{ongoing_count}</div>
            <div class="count-label">Ongoing Projects</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="count-card">
            <div style="font-size: 2rem; color: #1E5AF5; margin-bottom: 5px;">✅</div>
            <div class="count-value">{completed_count}</div>
            <div class="count-label">Completed Projects</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class="count-card">
            <div style="font-size: 2rem; color: #FF5252; margin-bottom: 5px;">⚠️</div>
            <div class="count-value">{critical_count}</div>
            <div class="count-label">Critical Timeline</div>
            <div style="font-size: 0.75rem; color: #888; margin-top: 5px;">Less than 60 days</div>
        </div>
        """, unsafe_allow_html=True)

def display_summary_cards(summary_data):
    """Display summary cards with key metrics"""
    
    # Section header
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
        <h3 style="margin: 0; color: #0A2463; font-size: 1.2rem;">Key Performance Indicators</h3>
        <div style="font-size: 0.9rem; color: #666;">Last updated: Mar 21, 2025</div>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(4)
    
    # Total Budget
    with cols[0]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">💰</div>
            <div class="metric-value">${summary_data['total_budget']/1000000:.2f}M</div>
            <div class="metric-label">Total Budget</div>
            <div style="font-size: 0.8rem; color: #66BB6A; margin-top: 5px; display: flex; align-items: center; justify-content: center;">
                <span style="margin-right: 3px;">↑</span> 12% from last year
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Projects Count
    with cols[1]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">📊</div>
            <div class="metric-value">{summary_data['projects_count']}</div>
            <div class="metric-label">Total Projects</div>
            <div style="height: 20px;"></div>
        </div>
        """, unsafe_allow_html=True)
    
    # Households Reached
    with cols[2]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🏡</div>
            <div class="metric-value">{summary_data['households_reached']}</div>
            <div class="metric-label">Households Reached</div>
            <div style="font-size: 0.8rem; color: #66BB6A; margin-top: 5px; display: flex; align-items: center; justify-content: center;">
                <span style="margin-right: 3px;">↑</span> 8% increase
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Individuals Reached
    with cols[3]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">👨‍👩‍👧‍👦</div>
            <div class="metric-value">{summary_data['individuals_reached']}</div>
            <div class="metric-label">Individuals Reached</div>
            <div style="font-size: 0.8rem; color: #66BB6A; margin-top: 5px; display: flex; align-items: center; justify-content: center;">
                <span style="margin-right: 3px;">↑</span> 15% increase
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_project_table(df):
    """Display the projects table with all details"""
    
    # Section header
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin: 30px 0 15px 0;">
        <h3 style="margin: 0; color: #0A2463; font-size: 1.2rem;">Project Details</h3>
        <div style="font-size: 0.9rem; color: #666;">Showing <span style="font-weight: 600; color: #0A2463"></span> projects</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Legend section for color coding
    st.markdown("""
    <div class="color-definition-container">
        <div class="color-definition-title">Timeline Color Legend:</div>
        <div class="color-definition">
            <div class="color-item"><div class="color-dot red-dot"></div> <span>Less than 60 days remaining</span></div>
            <div class="color-item"><div class="color-dot orange-dot"></div> <span>60-120 days remaining</span></div>
            <div class="color-item"><div class="color-dot green-dot"></div> <span>More than 120 days remaining</span></div>
            <div class="color-item"><div class="color-dot black-dot"></div> <span>Closed projects</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Table header
    st.markdown(f"""
    <div class="projects-table">
        <div class="table-header">
            <div class="projects-overview-title">Projects List ({len(df)} items)</div>
        </div>
        <div class="column-headers" style="display: grid; grid-template-columns: 1.5fr 1fr 0.8fr 0.8fr 0.8fr 0.8fr 0.8fr 1.5fr; gap: 10px;">
            <div>Project Manager</div>
            <div>Project Name</div>
            <div style="text-align: center;">Status</div>
            <div style="text-align: right;">Budget</div>
            <div style="text-align: center;">Remaining Time</div>
            <div>Start Date</div>
            <div>End Date</div>
            <div>Progress</div>
        </div>
    """, unsafe_allow_html=True)
    
    # No data message if dataframe is empty
    if len(df) == 0:
        st.markdown("""
        <div style="padding: 30px 0; text-align: center; color: #666;">
            <div style="font-size: 3rem; margin-bottom: 10px;">📊</div>
            <div style="font-weight: 500; margin-bottom: 5px;">No projects found</div>
            <div style="font-size: 0.9rem;">Try adjusting your filter criteria</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Table rows
    for _, row in df.iterrows():
        status_html = f'<span class="status-badge {row["status_color"]}" style="display: inline-block; text-align: center;">{row["status"]}</span>'
        
        # Create time circle based on remaining time
        time_class = ""
        if row['status'] == 'Closed':
            time_html = f'<div class="time-circle" style="background-color: #212121; margin: 0 auto;">0%</div>'
        else:
            if row['remaining_time_pct'] < 30:
                time_class = "time-red"
            elif row['remaining_time_pct'] < 60:
                time_class = "time-orange"
            else:
                time_class = "time-green"
            time_html = f'<div class="time-circle {time_class}" style="margin: 0 auto;">{row["remaining_time_pct"]}%</div>'
        
        # Avatar and project manager - improved with random background colors based on name
        initials = row['project_manager'][0].upper()
        bg_colors = ['#4285F4', '#EA4335', '#FBBC05', '#34A853', '#8523FA', '#20C997', '#9B59B6']
        color_index = hash(row['project_manager']) % len(bg_colors) 
        bg_color = bg_colors[color_index]
        
        manager_html = f"""
        <div class="avatar-container">
            <div style="background-color: {bg_color}; width: 32px; height: 32px; border-radius: 50%; margin-right: 10px; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 500; color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                {initials}
            </div>
            <div style="font-weight: 500;">{row['project_manager']}</div>
        </div>
        """
        
        # Progress bar with percentage - improved styling
        progress_pct = row['progress_pct']
        progress_color = "#0A2463"  # Default blue
        
        # Adjust color based on progress vs remaining time
        if row['status'] != 'Closed':
            if row['remaining_time_pct'] < 30 and progress_pct < 70:
                progress_color = "#FF5252"  # Red for warning
            elif row['remaining_time_pct'] < 60 and progress_pct < 50:
                progress_color = "#FFA726"  # Orange for caution
        
        progress_html = f"""
        <div style="position: relative; height: 8px; width: 100%; background-color: #eaecef; border-radius: 20px; overflow: hidden;">
            <div style="width: {progress_pct}%; height: 100%; background-color: {progress_color}; border-radius: 20px;"></div>
            <div style="position: absolute; right: 0; top: -18px; font-size: 12px; color: #555; font-weight: 500;">{progress_pct}%</div>
        </div>
        """
        
        # Format the row with hover effect
        row_html = f"""
        <div class="project-row" style="display: grid; grid-template-columns: 1.5fr 1fr 0.8fr 0.8fr 0.8fr 0.8fr 0.8fr 1.5fr; gap: 10px; align-items: center; padding: 14px 10px; border-bottom: 1px solid #f0f0f0; border-radius: 4px;">
            <div>{manager_html}</div>
            <div style="font-weight: 500; color: #0A2463;">{row['project_name']}</div>
            <div style="text-align: center;">{status_html}</div>
            <div style="text-align: right; font-weight: 500;">${row['budget']:,}</div>
            <div style="text-align: center;">{time_html}</div>
            <div style="color: #555;">{row['start_date']}</div>
            <div style="color: #555;">{row['end_date']}</div>
            <div>{progress_html}</div>
        </div>
        """
        
        st.markdown(row_html, unsafe_allow_html=True)
    
    # Close the table container
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add summary at the bottom if there's data
    if len(df) > 0:
        active_projects = len(df[df['status'] != 'Closed'])
        total_budget = df['budget'].sum()
        
        st.markdown(f"""
        <div style="margin-top: 15px; font-size: 0.9rem; color: #555; text-align: right;">
            Showing {len(df)} projects ({active_projects} active) with a combined budget of <span style="font-weight: 600; color: #0A2463">${total_budget:,}</span>
        </div>
        """, unsafe_allow_html=True)
