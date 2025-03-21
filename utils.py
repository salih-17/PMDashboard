def apply_filters(df, filter_params):
    """
    Apply filters to the dataframe based on selected filter parameters
    """
    filtered_df = df.copy()
    
    # Filter by project manager
    if filter_params['manager'] != 'All':
        filtered_df = filtered_df[filtered_df['project_manager'] == filter_params['manager']]
    
    # Filter by project name
    if filter_params['project'] != 'All':
        filtered_df = filtered_df[filtered_df['project_name'] == filter_params['project']]
    
    # Filter by status
    if filter_params['status'] != 'All':
        filtered_df = filtered_df[filtered_df['status'] == filter_params['status']]
    
    # Filter by timeline flag
    if filter_params['timeline'] != 'All':
        if filter_params['timeline'] == 'Closed':
            filtered_df = filtered_df[filtered_df['status'] == 'Closed']
        elif filter_params['timeline'] == 'Red':
            filtered_df = filtered_df[(filtered_df['status'] != 'Closed') & (filtered_df['days_remaining'] < 60)]
        elif filter_params['timeline'] == 'Orange':
            filtered_df = filtered_df[(filtered_df['status'] != 'Closed') & 
                                 (filtered_df['days_remaining'] >= 60) & 
                                 (filtered_df['days_remaining'] < 120)]
        elif filter_params['timeline'] == 'Green':
            filtered_df = filtered_df[(filtered_df['status'] != 'Closed') & (filtered_df['days_remaining'] >= 120)]
    
    return filtered_df
