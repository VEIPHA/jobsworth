from src.services.db_reader import read_raw_jobs
from src.services.db_writer import write_enriched_job_to_postgres
from src.handlers.row_enricher import enrich_job_row

def main():
    print("[ENRICH] EnrichmentAgent starting...")

    jobs = read_raw_jobs()
    print(f"[ENRICH] Loaded {len(jobs)} raw jobs")

    for idx, job in enumerate(jobs, 1):
        if not isinstance(job, dict):
            print(f"[ENRICH ERROR] Skipping invalid job at index {idx}: {type(job)} - {job}")
            continue

        print(f"[ENRICH] → [{idx}/{len(jobs)}] Enriching job: {job.get('job_title', 'Unknown Title')}")

        enriched = enrich_job_row(job)

        if enriched:
            print(f"[ENRICH] ✅ Enriched job: {enriched['cleaned_job_title']} | Rarity: {enriched['rarity']} | Salary: {enriched['estimated_salary']}")
            write_enriched_job_to_postgres(enriched)
        else:
            print(f"[ENRICH ERROR] ❌ Failed to enrich job: {job.get('job_title', 'Unknown Title')}")

    print("[ENRICH] EnrichmentAgent finished.")

if __name__ == "__main__":
    main()
