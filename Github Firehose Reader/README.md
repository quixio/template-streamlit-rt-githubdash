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
output = github-data
Quix__Broker__Address = localhost:19092
```


