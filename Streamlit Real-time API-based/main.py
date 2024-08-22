import streamlit as st
import requests
import time
import pandas as pd
import os
import logging
from datetime import datetime
import plotly.express as px

from dotenv import load_dotenv
load_dotenv() ### for local dev, outside of docker, load env vars from a .env file

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
st.title("Real-time Dashboard for GitHub Data using Streamlit,Flask and Quix")
st.markdown("This dashboard reads from a table via an API, which is being continuously updated by a Quix Streams sink process running in Docker. It then displays a dynamically updating Plotly chart and table underneath.")
st.markdown("In the backend, there are services that:\n * Read from the GitHub Firehose \n * Stream the event data to Redpanda\n * Read from Redpanda and aggregate the events per GitHub user\n * Sinking the page event counts (which are continuously updating) to PostGres\n\n ")
st.markdown("Take a closer a look at the [back-end code](https://github.com/quixio/template-streamlit-rt-githubdash), and learn how to read from a real-time source and apply some kind of transformation to the data before bringing it into Streamlit (using only Python)")

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
    fig = px.bar(df, x='displayname', y='event_count', title="Current Top 10 active GitHub Users by event count",
                 range_y=[min_scale, max_scale])

    # Style the chart
    fig.update_layout(
        xaxis_title="Display Name",
        yaxis_title="Event Count",
        xaxis=dict(tickangle=-90)  # Vertical label orientation
    )

    # Display the Plotly chart in Streamlit using st.plotly_chart
    chart_placeholder.plotly_chart(fig, use_container_width=True)

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
