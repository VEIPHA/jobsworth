from datetime import datetime
from src.boards.fractionaljobs import scrape_fractionaljobs
from src.boards.weworkremotely import scrape_wwr
from src.google_sheets import write_jobs_to_sheet

def run_all_scrapers():
    jobs = []
    for scraper in [scrape_fractionaljobs, scrape_wwr]:
        try:
            scraped = scraper()
            jobs.extend(scraped)
        except Exception as e:
            print(f"[ERROR] {scraper.__name__} failed: {e}")
    return jobs

if __name__ == "__main__":
    all_jobs = run_all_scrapers()

    # Add UTC timestamp to all jobs
    for job in all_jobs:
        job["date_posted"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

    write_jobs_to_sheet(
        jobs=all_jobs,
        creds_path="creds/gsheets-creds.json",
        sheet_name="jobscraper",
        tab_name="Jobs"
    )
