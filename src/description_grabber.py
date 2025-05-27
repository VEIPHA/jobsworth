import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from src.grabbers.fractionaljobs_grabber import grab_fractional_description

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

# === MAIN FUNCTION ===
def enrich_descriptions():
    sheet = get_sheet("jobscraper", "Jobs")
    data = sheet.get_all_records()

    urls = [row["url"] for row in data]
    descriptions = []

    print(f"[INFO] Fetching descriptions for {len(urls)} URLs...")

    for i, url in enumerate(urls):
        desc = grab_fractional_description(url)
        descriptions.append([desc])
        print(f"[{i+1}/{len(urls)}] Got description from {url}")

    # Add/update the Description column
    col_index = len(data[0]) + 1  # write after existing columns
    sheet.update_cell(1, col_index, "description")  # write header
    range_name = f"{chr(64 + col_index)}2:{chr(64 + col_index)}{len(descriptions) + 1}"
    sheet.update(range_name=range_name, values=descriptions)

if __name__ == "__main__":
    enrich_descriptions()
