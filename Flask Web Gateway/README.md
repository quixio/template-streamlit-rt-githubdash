# Flask Web Gateway

This service demonstrates how to run a Flask web gateway and use it to query a Postgres database.

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


