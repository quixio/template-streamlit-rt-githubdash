# Streamlit Dashboard

This service polls the data API and renders the resulting data in a Streamlit Dashboard with a simple chart and table. When running, it is accessable under: http://localhost:8031.

It connects to Redpanda or Kafka and reads from the input topic (the aggregated event counts), and inserts them into a database table.

This is the main function that gets the data from the API:

```python
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
```
* **NOTE**: Right now, the column names are hard-coded, so if you want to insert data with another structure or set of column names,  you need to update this query.

# Environment variables

Here is the one default environment variabe which you can find in the `.env` file.

```
API_URL = http://localhost/events
```

# Output

Here's a preview of the dashboard:

![GitHubstats](https://github.com/user-attachments/assets/c3f1c9d9-e48e-470c-902f-9152be57aec1)


