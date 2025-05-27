import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from src.grabbers.fractionaljobs_grabber import grab_fractional_description

def get_credentials_from_env():
    raw_json = os.getenv("GCP_CREDENTIALS_JSON")
    if not raw_json:
        raise ValueError("Missing GCP_CREDENTIALS_JSON")
    return json.loads(raw_json)

def update_descriptions(sheet_name="jobscraper", tab_name="Jobs"):
    print("[DESC] Connecting to Google Sheet...")
    creds_dict = get_credentials_from_env()
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).worksheet(tab_name)

    rows = sheet.get_all_records()
    header = sheet.row_values(1)

    # Ensure description column exists
    if "description" not in header:
        header.append("description")
        sheet.update_cell(1, len(header), "description")

    desc_col = header.index("description") + 1
    url_col = header.index("url") + 1
    source_col = header.index("source") + 1

    for idx, row in enumerate(rows, start=2):  # start=2 for header offset
        if row.get("source") != "fractionaljobs":
            continue
        if row.get("description"):
            continue

        job_url = row.get("url")
        print(f"[DESC] Grabbing description for row {idx}: {job_url}")
        desc = grab_fractional_description(job_url)
        sheet.update_cell(idx, desc_col, desc)

    print("[DESC] Finished updating job descriptions.")

if __name__ == "__main__":
    update_descriptions()
