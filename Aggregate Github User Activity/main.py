import os
from quixstreams import Application, State
from quixstreams.kafka.configuration import ConnectionConfig
from dotenv import load_dotenv

# for local dev, load env vars from a .env file
load_dotenv()

# Initialize the Quix Application with the connection configuration
app = Application(consumer_group=os.getenv("consumer_group_name","default-consumer-group"),
                  auto_offset_reset="earliest")

input_topic = app.topic(os.getenv("input","raw_data"))
output_topic = app.topic(os.getenv("output","processed_data"))
sdf = app.dataframe(input_topic)

# Get just the "actor" data out of the larger JSON message and use it as the new streaming dataframe
sdf = sdf.apply(
    lambda data: {
        "displayname": data['actor']['display_login'],
        "id": data['actor']['id']
    }
)

# Group (aka "Re-key") the streaming data by displayname so we can count the events
sdf = sdf.group_by("displayname")

# Counts the number of events by displayname
def count_messages(value: dict, state: State):
    current_total = state.get('event_count', default=0)
    current_total += 1
    state.set('event_count', current_total)
    return current_total

# Adds the message key (displayname) to the message body too (not that necessary, it's just for convenience)
def add_key_to_payload(value, key, timestamp, headers):
    value['displayname'] = key
    return value

# Start manipulating the streaming dataframe
sdf["event_count"] = sdf.apply(count_messages, stateful=True) # Apply the count function and store the results in an "event_count" column
sdf = sdf[["event_count"]] # Cut down our streaming dataframe to consist of JUST the event count
sdf = sdf.apply(add_key_to_payload, metadata=True) # Adding the key (displayname) to the payload so that its easier to see what user each event count belongs to.
sdf = sdf.filter(lambda row: row['displayname'] not in ['github-actions', 'direwolf-github', 'dependabot']) # Filter out what looks like bot accounts from the data

sdf = sdf.update(lambda row: print(f"Received row: {row}")) # Print each row so that we can see what we're going to send to the downstream topic

# Produce our processed streaming dataframe to the downstream topic "event_counts"
sdf = sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run(sdf)