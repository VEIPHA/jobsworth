# Jobsworth

Scrapes job posts from remote job boards and writes them to a Google Sheet.

## Setup

1. Clone the repo  
2. Add your Google credentials JSON as `creds/gsheets-creds.json`  
3. Install dependencies:

```bash
pip install -r requirements.txt

## Run

python -m src.scraper

## Structure

jobsworth/
├── creds/
│   └── gsheets-creds.json
├── src/
│   ├── boards/
│   │   ├── fractionaljobs.py
│   │   └── weworkremotely.py
│   ├── google_sheets.py
│   └── scraper.py
├── requirements.txt
└── README.md

## License

This project is open source under the MIT License.
You’re free to use, modify, and distribute it — just keep the original license and credit intact.
