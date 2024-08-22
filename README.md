A basic data pipeline that powers a streamlit Dashboard showing real-time counts for the top active users on GitHub.

![image](https://github.com/user-attachments/assets/f24e6f4e-29f6-453e-b67a-a5b7708304e5)



Here’s very brief breakdown of what each service does:

 * **Streamlit Dash Service**: Displays a Streamlit Dashboard which polls the API and renders the data a chart and table (when running, its available under: http://localhost:8031)
 
 *  **Flask API**: Uses Flask to serves a minimal REST API that can query a database and return the results as JSON.
 
 *  **Postgres Database**: Stores the continuously updating event count data. The Data API queries this database.
 
 * **Writer Service**: Reads from a topic and continuously updates the database with new data.
 
 * **Aggregation Service**: Refines the raw event logs and continuously aggregates them into event counts broken down by GitHub display name.
 
 * **Streaming Data Producer**: Reads from a real time public feed of activity on GitHub and streams the data to a topic in Redpanda (our local message broker)
 
 * **Red Panda Server**: Manages the flow of streaming data via topics (buffers for streaming data).
