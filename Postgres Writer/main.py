import psycopg2
import logging
import os
from quixstreams import Application
from quixstreams.kafka.configuration import ConnectionConfig

from dotenv import load_dotenv
load_dotenv() ### for local dev, outside of docker, load env vars from a .env file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Using broker address: {os.getenv('Quix__Broker__Address')}")

# Initialize the Quix Application with the connection configuration
app = Application(consumer_group="count-consumer-v1",
                  auto_offset_reset="earliest")

input_topic = app.topic(os.getenv("input","processed_data")) # Define the input topic to consume from
sdf = app.dataframe(input_topic) # Turn the data from the input topic into a streaming dataframe

# PostgreSQL connection details
pg_host = os.environ['PG_HOST']
pg_port = os.getenv('PG_PORT','5432')
pg_db = os.environ['PG_DATABASE']
pg_user = os.environ['PG_USER']
pg_password = os.environ['PG_PASSWORD']
tablename = os.getenv("PG_TABLE","page_counts") # The name of the table we want to write to

logger.info(f"Using Postgres server address: {pg_host}, port '{pg_port}',database '{pg_db}', user '{pg_user}', user '{pg_password}', table '{tablename }'")

# Establish a connection to PostgreSQL
conn = psycopg2.connect(
    host=pg_host,
    port=pg_port,
    database=pg_db,
    user=pg_user,
    password=pg_password
)

try:
    # Do a basic check if the target table exists and create it if not
    with conn.cursor() as cursor:
        cursor.execute(f"""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = '{tablename}'
            );
        """)
        table_exists = cursor.fetchone()[0]
        if not table_exists:
            cursor.execute(f'''
                CREATE TABLE {tablename} (
                    displayname VARCHAR UNIQUE,
                    event_count INTEGER
                );
            ''')
        conn.commit()
except psycopg2.Error as e:
    logger.error(f"Error checking/creating table: {e}")
    raise

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

app.run(sdf)
