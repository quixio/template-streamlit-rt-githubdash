A basic data pipeline that powers a streamlit Dashboard showing real-time counts for the top active users on GitHub.

![image](https://github.com/user-attachments/assets/f24e6f4e-29f6-453e-b67a-a5b7708304e5)



Here’s very brief breakdown of what each service does:

 * **[Streamlit Dash Service](./Streamlit%20Real-time%20API-based/README.md)**: Displays a Streamlit Dashboard which polls the API and renders the data a chart and table (when running, its available under: http://localhost:8031)
 
 * **[Data API**](./Flask%20Web%20Gateway/README.md): Uses Flask to serves a minimal REST API that can query a database and return the results as JSON.
 
 * **[Postgres Database**](./Demo%20PostgreSQL%20Database/README.md): Stores the continuously updating event count data. The Data API queries this database.
 
 * **[Posrgres Writer Service](./Postgres%20Writer/README.md)**: Reads from a topic and continuously updates the database with new data.
 
 * **[Aggregation Service](./Aggregate%20Github%20User%20Activity/README.md)**: Refines the raw event logs and continuously aggregates them into event counts broken down by GitHub display name.
 
 * **[Streaming Data Producer](./Github%20Firehose%20Reader/README.md)**: Reads from a real time public feed of activity on GitHub and streams the data to a topic in Redpanda (our local message broker)
 
 * **Red Panda Server**: Manages the flow of streaming data via topics (buffers for streaming data).
