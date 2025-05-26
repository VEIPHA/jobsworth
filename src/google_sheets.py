import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def write_jobs_to_sheet(jobs, sheet_name, tab_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Load secret parts from env vars
    private_key = os.getenv("GCP_PRIVATE_KEY").replace("\\n", "\n")
    
    creds_dict = {
        "type": "service_account",
        "project_id": "jobscraper-460818",
        "private_key_id": "d3651a17fbe96911eea0b644860e70fec9e0ff6b",
        "private_key": private_key,
        "client_email": "jobscraper@jobscraper-460818.iam.gserviceaccount.com",
        "client_id": "103019541166983160511",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/jobscraper@jobscraper-460818.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    sheet = client.open(sheet_name).worksheet(tab_name)
    header = list(jobs[0].keys()) if jobs else []
    rows = [list(job.values()) for job in jobs]

    sheet.clear()
    sheet.append_row(header)
    for row in rows:
        sheet.append_row(row)
