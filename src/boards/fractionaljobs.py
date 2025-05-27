from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_fractionaljobs():
    print("[INFO] Starting fractionaljobs scraper...")

    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.fractionaljobs.io/#jobs", timeout=60000)
        page.wait_for_timeout(3000)  # allow JS content to load
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    job_items = soup.select(".job-item")
    print(f"[INFO] Found {len(job_items)} job elements")

    for job in job_items:
        try:
            name_url_block = job.select_one(".job-item_name_url")
            if not name_url_block:
                continue

            h3_elements = name_url_block.select("h3.text-size-regular.text-inline")
            if len(h3_elements) < 3:
                continue

            company = h3_elements[0].get_text(strip=True)
            title = h3_elements[2].get_text(strip=True)

            job_link = job.select_one(".job-item_link-to-job")
            if job_link and job_link.get('href'):
                job_url = job_link['href']
                if job_url.startswith('/'):
                    job_url = "https://www.fractionaljobs.io" + job_url
                elif not job_url.startswith('http'):
                    job_url = "https://www.fractionaljobs.io/" + job_url
            else:
                company_link = job.select_one(".job-item_company-link")
                job_url = company_link['href'] if company_link and company_link.get('href') else "https://www
