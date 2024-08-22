A basic data pipeline that powers a streamlit Dashboard showing real-time counts for the top active users on GitHub.

![image](https://github.com/user-attachments/assets/6af7e480-75d0-47c5-ae3f-939c8ba86e09)


Here’s very brief breakdown of what each service does:

 * Streamlit Service: Displays a Streamlit Dashboard which polls the API and renders the data a chart and table.
 
 *  Flask API: Serves a minimal REST API that can query a database and return the results as JSON.
 
 *  Postgres Database: Stores the event count data.
 
 * Writer Service: Reads from a topic and continuously updates the database with new data.
 
 * Aggregation Service: Refines the raw event logs and continuously aggregates them into event counts broken down by GitHub display name.
 
 * Streaming Data Producer: Reads from a real time public feed of activity on GitHub and streams the data to a topic in Redpanda (our local message broker)
 
 *  Red Panda Server: Manages the flow of streaming data via topics (buffers for streaming data).
