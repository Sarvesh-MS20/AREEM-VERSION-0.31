#db/db.py
import psycopg2

def get_connection():
    connection = psycopg2.connect(
        dbname = "agent_system_one",
        user = "postgres",
        host = "localhost",
        password = "sarvesh20",
        port = "5432"
    )
    return connection