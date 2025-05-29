from src.services.db_reader import read_raw_jobs
from src.services.db_writer import write_enriched_job_to_postgres
from src.handlers.row_enricher import enrich_job_row

def main():
    print("[ENRICH] EnrichmentAgent starting...")

    jobs = read_raw_jobs()
    print(f"[ENRICH] Loaded {len(jobs)} raw jobs")

   for job in jobs:
    if not isinstance(job, dict):
        print(f"[ENRICH ERROR] Skipping invalid job: {type(job)} - {job}")
        continue  # skip to the next one

    enriched = enrich_job_row(job)
    if enriched:
        write_enriched_job_to_postgres(enriched)

    print("[ENRICH] EnrichmentAgent finished")

if __name__ == "__main__":
    main()
