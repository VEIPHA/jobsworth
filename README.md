# Jobsworth

Jobsworth is a lightweight, AI-powered job aggregator. It scrapes remote/flexible job listings from multiple public sources, cleans and enriches the data, and publishes it to a Google Sheet. Future phases include semantic search, a UI, and a public API.

---

## 🛠 Features

- Scrapes jobs from FractionalJobs.io and WeWorkRemotely (more to come)
- Cleans and standardises job data
- Writes jobs to a Google Sheet via service account
- Modular agent-based architecture (planned)

---

## 📦 Requirements

- Python 3.9+
- `gspread`
- `oauth2client`
- `beautifulsoup4`
- `requests`
- Google Service Account credentials (JSON)

---

## 🚀 Quick Start

1. Clone the repo:
   ```bash
   git clone https://github.com/VEIPHA/jobsworth.git
   cd jobsworth
