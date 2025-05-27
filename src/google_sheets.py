import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_credentials_from_env():
    raw_key = os.getenv("GCP_PRIVATE_KEY", "").replace("\\n", "\n")
    if not raw_key:
        raise ValueError("Missing GCP_PRIVATE_KEY")

    creds_dict = {
        "type": "service_account",
        "project_id": "jobscraper-460818",
        "private_key_id": "your-private-key-id",
        "private_key": raw_key,
        "client_email": "jobscraper@jobscraper-460818.iam.gserviceaccount.com",
        "client_id": "103019541166983160511",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/jobscraper%40jobscraper-460818.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }
    return creds_dict

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
    sheet.append_row(header)
    for row in rows:
        sheet.append_row(row)
