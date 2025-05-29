import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_credentials_from_env():
    raw_json = os.getenv("GCP_CREDENTIALS_JSON")
    if not raw_json:
        raise ValueError("Missing GCP_CREDENTIALS_JSON")
    return json.loads(raw_json)

def write_jobs_to_sheet(jobs, sheet_name, tab_name):
    if not jobs:
        print("[SHEET] No jobs to write.")
        return

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_dict = get_credentials_from_env()
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    sheet = client.open(sheet_name).worksheet(tab_name)
    header = sorted(jobs[0].keys())  
    rows = [[job.get(col, "") for col in header] for job in jobs]

    sheet.clear()
    sheet.append_rows([header] + rows, value_input_option="USER_ENTERED")
    print(f"[SHEET] ✅ Wrote {len(jobs)} jobs to Google Sheet: {sheet_name} -> {tab_name}")

def read_jobs(sheet_name, tab_name):
    """Fetch all rows from the sheet as a list of dicts."""
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_dict = get_credentials_from_env()
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    sheet = client.open(sheet_name).worksheet(tab_name)
    records = sheet.get_all_records()
    return records, sheet

def update_description(sheet, row_index, description):
    """
    Update the 'description' cell in the given row.
    Note: row_index is 0-based for get_all_records() (excluding header),
    so we use row_index + 2 to account for the header and 1-based indexing.
    """
    sheet.update_cell(row_index + 2, 8, description)  # Column 8 = 'H'
