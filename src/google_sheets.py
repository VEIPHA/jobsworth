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
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_dict = get_credentials_from_env()
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    sheet = client.open(sheet_name).worksheet(tab_name)
    header = list(jobs[0].keys()) if jobs else []
    rows = [list(job.values()) for job in jobs]

    sheet.clear()
    sheet.append_rows([header] + rows, value_input_option="USER_ENTERED")
