from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrape_wwr():
    print("[WWR] Starting scrape...")
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print("[WWR] Navigating to page...")
        page.goto("https://weworkremotely.com/", timeout=60000)

        # Wait for job listings to appear (adjust if needed)
        try:
            page.wait_for_selector("li.new-listing-container", timeout=10000)
        except Exception as e:
            print(f"[WWR] Timeout waiting for job listings: {e}")

        html = page.content()
        browser.close()

    # Optional: dump partial HTML to debug
    print("[WWR] Dumping first 2000 characters of HTML...")
    print(html[:2000])

    soup = BeautifulSoup(html, "html.parser")
    listings = soup.select("li.new-listing-container")
    print(f"[WWR] Found {len(listings)} job <li> elements")

    for li in listings:
        try:
            a_tag = li.find("a", href=True)
            job_url = f"https://weworkremotely.com{a_tag['href']}" if a_tag else None

            title_tag = li.select_one("h4.new-listing__header__title")
            company_tag = li.select_one("p.new-listing__company-name")
            region_tag = li.select_one("p.new-listing__company-headquarters")

            if not (job_url and title_tag and company_tag):
                continue

            jobs.append({
                "title": title_tag.text.strip(),
                "company": company_tag.text.strip(),
                "region": region_tag.text.strip() if region_tag else "Unknown",
                "url": job_url,
                "source": "weworkremotely"
            })

        except Exception as e:
            print(f"[WWR] Error parsing job listing: {e}")
            continue

    print(f"[WWR] scrape_wwr returned {len(jobs)} jobs.")
    if jobs:
        print("[WWR] Example job:", jobs[0])
    return jobs
