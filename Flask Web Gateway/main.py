import os
from flask import Flask, jsonify
from waitress import serve
import psycopg2
import logging

# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Replace with your PostgreSQL connection details
pg_host = os.environ['PG_HOST']
pg_db = os.environ['PG_DATABASE']
pg_user = os.environ['PG_USER']
pg_password = os.environ['PG_PASSWORD']
pg_table = os.environ['PG_TABLE']

# Establish a connection to PostgreSQL
conn = psycopg2.connect(
    host=pg_host,
    database=pg_db,
    user=pg_user,
    password=pg_password
)

@app.route('/events', methods=['GET'])
def get_user_events():
    query = f"SELECT * FROM {pg_table} ORDER BY event_count DESC LIMIT 10"

    logger.info(f"Running query: {query}")

    try:
        # Execute the query
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

        # Convert the result to a list of dictionaries
        results_list = [dict(zip(columns, row)) for row in results]
    except:
        logger.info(f"Error querying Postgres...")
        results_list = [{"error": "Database probably not ready yet."}]

    return jsonify(results_list)

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=80)