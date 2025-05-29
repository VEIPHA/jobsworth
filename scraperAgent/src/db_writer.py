import os
import psycopg2

def write_job_to_postgres(job):
    try:
        conn = psycopg2.connect(os.getenv("PG_CONN_STRING"))
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO raw_jobs (
            job_title, company_name, region, job_url,
            source, timestamp, date_posted, raw_description
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (
            job["title"],
            job["company"],
            job["region"],
            job["url"],
            job["source"],
            job["timestamp"],
            job["date_posted"],
            job.get("description", "")
        ))

        conn.commit()
        cursor.close()
        conn.close()
        print(f"[DB] ✅ Job written to Postgres: {job['title']}")

    except Exception as e:
        print(f"[DB] ❌ Failed to write job to Postgres: {e}")
