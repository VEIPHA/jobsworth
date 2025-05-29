import os
import psycopg2

def write_enriched_job_to_postgres(job):
    try:
        conn = psycopg2.connect(os.getenv("PG_CONN_STRING"))
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO enriched_jobs (
            cleaned_job_title, company_name, company_summary,
            job_summary, job_URL, job_category,
            source, region, estimated_salary,
            rarity, created_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (
            job["cleaned_job_title"],
            job["company_name"],
            job["company_summary"],
            job["job_summary"],
            job["job_URL"],
            job["job_category"],
            job["source"],
            job["region"],
            job["estimated_salary"],
            job["rarity"],
            job["created_at"]
        ))

        conn.commit()
        cursor.close()
        conn.close()
        print(f"[DB] ✅ Enriched job written to Postgres: {job['cleaned_job_title']}")

    except Exception as e:
        print(f"[DB] ❌ Failed to write enriched job to Postgres: {e}")
