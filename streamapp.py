import streamlit as st
import pandas as pd
import re
from collections import Counter


# Assuming 'df' is loaded using the consolidation function above
# We will mock the data load here for the app structure
@st.cache_data
def load_data():
    # Replace with your actual consolidated data loading logic
    return pd.read_csv('Consolidated_Master_Data.csv') 

df = load_data()

st.title("Tutor Performance & Trend Analysis")

# 1. Global Slicer
tutor_list = df['Tutor'].dropna().unique().tolist()
selected_tutor = st.selectbox("Select a Tutor to Analyze:", tutor_list)

# Filter to the specific tutor
tutor_df = df[df['Tutor'] == selected_tutor].copy()

# 2. Time-Series Aggregation
# We need to calculate the average scores per month for this tutor
monthly_stats = tutor_df.groupby('Month').agg({
    'Overall Score %': 'mean',
    'Setup': 'mean',
    'Attitude': 'mean',
    'Preparation': 'mean',
    'Curriculum': 'mean',
    'Teaching': 'mean',
    'Feedback': 'mean'
}).reset_index()

# Sort chronologically to ensure we compare May to April
monthly_stats = monthly_stats.sort_values('Month')

# 3. UI: Display Performance Deltas
st.subheader("Performance Shift (Latest Month vs. Previous)")

if len(monthly_stats) >= 2:
    # Get the two most recent months
    current_month = monthly_stats.iloc[-1]
    previous_month = monthly_stats.iloc[-2]
    
    # Create rows of metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta_overall = current_month['Overall Score %'] - previous_month['Overall Score %']
        st.metric("Overall Quality (100)", f"{current_month['Overall Score %']:.1f}", f"{delta_overall:.1f}")
        
    with col2:
        delta_teaching = current_month['Teaching'] - previous_month['Teaching']
        st.metric("Teaching (5)", f"{current_month['Teaching']:.1f}", f"{delta_teaching:.1f}")
        
    with col3:
        delta_prep = current_month['Preparation'] - previous_month['Preparation']
        st.metric("Preparation (5)", f"{current_month['Preparation']:.1f}", f"{delta_prep:.1f}")
        
    with col4:
        delta_attitude = current_month['Attitude'] - previous_month['Attitude']
        st.metric("Attitude (5)", f"{current_month['Attitude']:.1f}", f"{delta_attitude:.1f}")

else:
    st.warning("Not enough historical data to show a month-over-month trend for this tutor.")
# 4. Processing Logic
def process_comments(comment_list):
    cleaned_comments = []
    for text in comment_list:
        lines = str(text).split('\n')
        for line in lines:
            clean_line = re.sub(r'^[-–—]\s*[A-Za-z]\s*[-–—]\s*', '', line).strip()
            if clean_line:
                cleaned_comments.append(clean_line)
    return Counter(cleaned_comments)

# CRITICAL FIX: Use tutor_df instead of df, and use the exact lowercase column names
positive_counts = process_comments(tutor_df['Positive Comments'].fillna('').tolist())
negative_counts = process_comments(tutor_df['Negative Comments'].fillna('').tolist())
# 5. UI: Display Results in Columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Positive Comments")
    for comment, count in positive_counts.most_common(10):
        if count > 0:
            st.success(f"**[{count}x]** {comment}")

with col2:
    st.subheader("Top Negative/Constructive Comments")
    for comment, count in negative_counts.most_common(10):
        if count > 0:
            st.error(f"**[{count}x]** {comment}")