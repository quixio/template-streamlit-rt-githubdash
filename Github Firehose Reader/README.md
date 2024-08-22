# Github Firehose Reader

Insprired by the video [High Performance Kafka Producers in Python](https://www.youtube.com/watch?v=mdhEXg5Pny8) from Kris Jenkins: 

It reads from the [GitHub Firehose](https://github-firehose.libraries.io/) using Server-Sent Events (SSE) and publishes that data to a topic in Apache Kafka or Redpanda.


## How to run

Install the requirements first:

`pip install -r requirements.txt`

Run the main application:

`python main.py`

## Default Environment variables

You can find these in the accompanying `.env` file.

```
input = event-counts
PG_HOST = localhost
PG_PORT = 5433
PG_USER = root
PG_DATABASE = test_db
PG_SCHEMA = public
PG_TABLE = event_counts
PG_PASSWORD = root
Quix__Broker__Address = localhost:19092
```


