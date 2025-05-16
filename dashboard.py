
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import ast

st.set_page_config(page_title="Sentiment & Topic Dashboard", layout="wide")
st.title("📊 Sentiment & Topic Dashboard")

# Load Data
review_df = pd.read_excel('review_sentiments.xlsx')
topic_df = pd.read_excel('topic_results.xlsx')

# Normalize sentiment column
review_df['sentiment'] = review_df['sentiment'].str.lower()

# Sentiment bar chart (clean)
positive_count = review_df[review_df['sentiment'] == 'positive'].shape[0]
negative_count = review_df[review_df['sentiment'] == 'negative'].shape[0]
total_count = positive_count + negative_count

st.subheader("Overall Sentiment Distribution")

if total_count > 0:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[negative_count],
        y=[''],
        orientation='h',
        marker=dict(color='rgba(220, 20, 60, 0.8)'),
        hoverinfo='skip',
    ))
    fig.add_trace(go.Bar(
        x=[positive_count],
        y=[''],
        orientation='h',
        marker=dict(color='rgba(34, 139, 34, 0.8)'),
        hoverinfo='skip',
    ))
    fig.update_layout(
        barmode='stack',
        height=30,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No sentiment data available.")

# Topic keywords
representation_topics = topic_df['Representation'].dropna().astype(str).tolist()
keywords = []
for rep in representation_topics:
    try:
        words = ast.literal_eval(rep)
        if isinstance(words, list):
            keywords.extend(words)
    except (ValueError, SyntaxError):
        continue

unique_keywords = sorted(set(keywords))
mid_index = len(unique_keywords) // 2
negative_keywords = unique_keywords[:mid_index]
positive_keywords = unique_keywords[mid_index:]

# Active keyword toggle
if 'active_keyword' not in st.session_state:
    st.session_state['active_keyword'] = None

# Layout columns: negative left, positive right with bigger spacing
col1, spacer, col2 = st.columns([1, 0.5, 1])

with col1:
    st.subheader("Negative Topics")
    neg_cols = st.columns(5)
    for i, keyword in enumerate(negative_keywords):
        with neg_cols[i % 5]:
            if st.button(keyword, key=f"neg_{keyword}"):
                if st.session_state['active_keyword'] == f"neg_{keyword}":
                    st.session_state['active_keyword'] = None
                else:
                    st.session_state['active_keyword'] = f"neg_{keyword}"

with col2:
    st.subheader("Positive Topics")
    pos_cols = st.columns(5)
    for i, keyword in enumerate(positive_keywords):
        with pos_cols[i % 5]:
            if st.button(keyword, key=f"pos_{keyword}"):
                if st.session_state['active_keyword'] == f"pos_{keyword}":
                    st.session_state['active_keyword'] = None
                else:
                    st.session_state['active_keyword'] = f"pos_{keyword}"

# Result display section
if st.session_state['active_keyword']:
    st.markdown("---")
    key = st.session_state['active_keyword']
    sentiment_type = 'negative' if key.startswith('neg_') else 'positive'
    keyword = key[4:]
    st.subheader(f"{sentiment_type.capitalize()} reviews mentioning '{keyword}':")
    filtered_reviews = review_df[
        (review_df['sentiment'] == sentiment_type) &
        (review_df['text'].str.contains(keyword, case=False, na=False))
    ]
    st.dataframe(filtered_reviews[['text']])
