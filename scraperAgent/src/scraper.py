print("[INFO] Starting scraper...", flush=True)

from datetime import datetime, timezone
from src.boards.fractionaljobs import scrape_fractionaljobs
from src.boards.weworkremotely import scrape_wwr
from src.google_sheets import write_jobs_to_sheet
from src.db_writer import write_job_to_postgres  

def run_all_scrapers():
    jobs = []
    for scraper in [scrape_fractionaljobs, scrape_wwr]:
        print(f"[INFO] Running scraper: {scraper.__name__}", flush=True)
        try:
            scraped = scraper()
            print(f"[INFO] {scraper.__name__} returned {len(scraped)} jobs", flush=True)
            jobs.extend(scraped)
        except Exception as e:
            print(f"[ERROR] {scraper.__name__} failed: {e}", flush=True)
    return jobs

if __name__ == "__main__":
    all_jobs = run_all_scrapers()

    for job in all_jobs:
        write_job_to_postgres(job)  

    print(f"[INFO] Writing {len(all_jobs)} jobs to sheet...", flush=True)

    write_jobs_to_sheet(
        jobs=all_jobs,
        sheet_name="jobscraper",
        tab_name="Jobs"
    )
