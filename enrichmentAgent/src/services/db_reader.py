import os
import psycopg2
import psycopg2.extras

def read_raw_jobs():
    try:
        conn = psycopg2.connect(os.getenv("PG_CONN_STRING"))
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute("SELECT * FROM raw_jobs ORDER BY id DESC LIMIT 100")  # tweakable
        jobs = cursor.fetchall()

        cursor.close()
        conn.close()

        print(f"[DB] ✅ Loaded {len(jobs)} raw jobs from Postgres")
        return jobs

    except Exception as e:
        print(f"[DB] ❌ Failed to read raw jobs: {e}")
        return []
