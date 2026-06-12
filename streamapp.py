import streamlit as st
import pandas as pd
import re
from collections import Counter

# 1. Load Data (Cache it so the app doesn't reload the file on every click)
@st.cache_data
def load_data():
    # Replace with your actual file path
    return pd.read_csv('may_analysis_v2 - May_more_95.csv') 

df = load_data()

# 2. UI: App Title and Slicer (Dropdown)
st.title("Tutor Performance & Feedback Analysis")
tutor_list = df['Tutor Name'].dropna().unique().tolist()
selected_tutor = st.selectbox("Select a Tutor to Analyze:", ["All Tutors"] + tutor_list)
st.set_page_config(
  page_title="Kirollos Aziz analysis",
)
# 3. Filter Data Based on Selection
if selected_tutor != "All Tutors":
    df = df[df['Tutor Name'] == selected_tutor]

# 4. Processing Logic (Same as before)
def process_comments(comment_list):
    cleaned_comments = []
    for text in comment_list:
        lines = str(text).split('\n')
        for line in lines:
            clean_line = re.sub(r'^[-–—]\s*[A-Za-z]\s*[-–—]\s*', '', line).strip()
            if clean_line:
                cleaned_comments.append(clean_line)
    return Counter(cleaned_comments)

positive_counts = process_comments(df['Positive comments'].fillna('').tolist())
negative_counts = process_comments(df['Negative comments'].fillna('').tolist())

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