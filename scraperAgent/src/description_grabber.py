import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from src.grabbers.fractionaljobs_grabber import grab_fractional_description
from src.grabbers.weworkremotely_grabber import grab_wwr_description

# === AUTH ===
def get_credentials_from_env():
    raw_json = os.getenv("GCP_CREDENTIALS_JSON")
    if not raw_json:
        raise ValueError("Missing GCP_CREDENTIALS_JSON")
    return json.loads(raw_json)

def get_sheet(sheet_name, tab_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = get_credentials_from_env()
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open(sheet_name).worksheet(tab_name)

# === SOURCE DISPATCH ===
def fetch_description(url: str, source: str) -> str:
    if source == "fractionaljobs":
        return grab_fractional_description(url)
    elif source == "weworkremotely":
        return grab_wwr_description(url)

    print(f"[SKIP] Source '{source}' is not yet configured for enrichment.")
    return "Not processed"

# === MAIN FUNCTION ===
def enrich_descriptions():
    sheet = get_sheet("jobscraper", "Jobs")
    data = sheet.get_all_records()

    print(f"[INFO] Processing {len(data)} rows from sheet...")

    descriptions = []

    for i, row in enumerate(data):
        url = row.get("url")
        source = row.get("source", "").lower()

        desc = fetch_description(url, source)
        descriptions.append([desc])
        print(f"[{i+1}/{len(data)}] Processed {source} – {url}")

    # Add/update the Description column
    col_index = len(data[0]) + 1  # assumes no existing description col
    sheet.update_cell(1, col_index, "description")
    range_name = f"{chr(64 + col_index)}2:{chr(64 + col_index)}{len(descriptions) + 1}"
    sheet.update(range_name=range_name, values=descriptions)

if __name__ == "__main__":
    enrich_descriptions()
