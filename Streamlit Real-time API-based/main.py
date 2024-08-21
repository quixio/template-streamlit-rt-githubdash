import streamlit as st
import requests
import time
import pandas as pd
import os
import logging
from datetime import datetime
import plotly.express as px
# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API endpoint URL
api_url = os.environ['API_URL']

## Function to get data from the API
def get_data():
    print(f"[{datetime.now()}] Fetching data from API...")
    response = requests.get(api_url)
    data = response.json()
    df = pd.DataFrame(data)

    try:
        # Reorder columns
        # df = df[['page_id', 'count']]
        df = df[['displayname', 'event_count']]
    except:
        logger.info("No data yet...")

    return df

# Function to get data and cache it
@st.cache_data
def get_cached_data():
    return get_data()

# Streamlit UI
st.title("Real-time Dashboard Example Using Streamlit and Quix")
st.markdown("This dashboard reads from a table via an API, which is being continuously updated by a sink process in Quix Cloud. It then displays a dynamically updating Bokeh chart and table underneath.")
st.markdown("In Quix Cloud, we are:\n * Generating synthetic user logs\n * Streaming the data to Kafka\n * Reading from Kafka and aggregating the actions per page\n * Sinking the page view counts (which are continuously updating) to MotherDuck\n\n ")
st.markdown("What users could learn: How to read from a real-time source and apply some kind of transformation to the data before bringing it into Streamlit (using only Python)")

# Placeholder for the bar chart and table
chart_placeholder = st.empty()
table_placeholder = st.empty()

# Placeholder for countdown text
countdown_placeholder = st.empty()

# Main loop
while True:
    # Get the data
    df = get_cached_data()

    # Check that data is being retrieved and passed correctly
    if df.empty:
        st.error("No data found. Please check your data source.")
        break

    # Calculate dynamic min and max scales
    min_count = df['event_count'].min()
    max_count = df['event_count'].max()
    min_scale = min_count * 0.99
    max_scale = max_count * 1.01

    # Create a Plotly figure
    fig = px.bar(df, x='displayname', y='event_count', title="Event Counts",
                 range_y=[min_scale, max_scale])

    # Style the chart
    fig.update_layout(
        xaxis_title="Display Name",
        yaxis_title="Event Count",
        xaxis=dict(tickangle=-90)  # Vertical label orientation
    )

    # Display the Plotly chart in Streamlit using st.plotly_chart
    chart_placeholder.plotly_chart(fig, use_container_width=True)

    st.markdown("**Current Top 10 active GitHub Users by event count**")
    # Display the dataframe as a table
    table_placeholder.table(df)

    # Countdown
    for i in range(1, 0, -1):
        countdown_placeholder.text(f"Refreshing in {i} seconds...")
        time.sleep(1)

    # Clear the countdown text
    countdown_placeholder.empty()

    # Clear the cache to fetch new data
    get_cached_data.clear()
