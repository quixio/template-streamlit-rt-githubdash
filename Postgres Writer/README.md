# Aggregate Github User Activity

This service reads from a Kafka topic and writes the entries to a Postgres db. 

It connects to Redpanda or Kafka and reads from the input topic (the aggregated event counts), and inserts them into a database table.

This is the main function that does the insertions

```python
def insert_data(conn, msg):
    # Insert data into the DB and if the displayname exists, update the count in the existing row
    with conn.cursor() as cursor:
        cursor.execute(f'''
            INSERT INTO {tablename} (displayname, event_count ) VALUES (%s, %s)
            ON CONFLICT (displayname)
            DO UPDATE SET event_count = EXCLUDED.event_count;
        ''', (msg['displayname'], msg['event_count']))
        conn.commit()
    logger.info(f"Wrote record: {msg}")

sdf = sdf.update(lambda val: insert_data(conn, val), stateful=False)
```
* **NOTE**: Right now, the column names are hard-coded, so if you want to insert data with another structure or set of column names,  you need to update this query.

Here's a preview of the log output:

```
INFO:__main__:Wrote record: {'event_count': 94, 'displayname': 'swa-runner-app'}
INFO:__main__:Wrote record: {'event_count': 2, 'displayname': 'hmrc-web-operations'}
INFO:__main__:Wrote record: {'event_count': 1, 'displayname': 'pranshu05'}
INFO:__main__:Wrote record: {'event_count': 1, 'displayname': 'SinghAstra'}
INFO:__main__:Wrote record: {'event_count': 1, 'displayname': 'Timidaniel'}
INFO:__main__:Wrote record: {'event_count': 18, 'displayname': 'JonathansManoel'}
INFO:__main__:Wrote record: {'event_count': 5, 'displayname': 'codacy-staging'}
INFO:__main__:Wrote record: {'event_count': 95, 'displayname': 'swa-runner-app'}
```

