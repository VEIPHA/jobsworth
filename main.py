from src.scraper import run_all_scrapers
from src.google_sheets import write_jobs_to_sheet

if __name__ == "__main__":
    # Run scrapers
    all_jobs = run_all_scrapers()

    # Write to Google Sheets
    write_jobs_to_sheet(
        jobs=all_jobs,
        creds_path="creds/gsheets-creds.json",  # adjust if stored elsewhere
        sheet_name="jobscraper",
        tab_name="Jobs")

