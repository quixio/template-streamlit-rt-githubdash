# Aggregate Github User Activity

This service keeps a running counts the events detect for each GitHub user using stateful calcuations. 

It connects to Redpanda or Kafka and reads from the input topic (the raw events from the GitHub Firehose), processes them, and sends the aggregations to the output topic for the Postgres WWriter to pick up.

This is the main function that does the calculation:

```python
# Group (aka "Re-key") the streaming data by displayname so we can count the events
sdf = sdf.group_by("displayname")

# Counts the number of events by displayname
def count_messages(value: dict, state: State):
    current_total = state.get('event_count', default=0)
    current_total += 1
    state.set('event_count', current_total)
    return current_total
```

It then sends messages to output topic. Here's a preview of the log output to give you an idea of the message format:

```
INFO:__main__:Sent row: {'event_count': 209, 'displayname': 'heimuhaha'}
INFO:__main__:Sent row: {'event_count': 1, 'displayname': 'spanky-the-elfbot'}
INFO:__main__:Sent row: {'event_count': 1, 'displayname': 'qulop'}
INFO:__main__:Sent row: {'event_count': 1, 'displayname': 'truongsinh'}
INFO:__main__:Sent row: {'event_count': 2, 'displayname': 'GeorgyKomkov'}
INFO:__main__:Sent row: {'event_count': 1, 'displayname': 'ImamHaris'}
INFO:__main__:Sent row: {'event_count': 1, 'displayname': 'yaroslavsysoiev'}
INFO:__main__:Sent row: {'event_count': 146, 'displayname': 'shullp05'}
```
The Postgres WWriter the reads these messages and inserts them into the Postgres DB.
