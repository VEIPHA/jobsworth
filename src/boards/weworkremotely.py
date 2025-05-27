from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrape_wwr():
    print("[WWR] Starting scrape...")
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )

        context = browser.new_context(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        ))

        page = context.new_page()
        print("[WWR] Navigating to page...")
        page.goto("https://weworkremotely.com/", timeout=60000)

        try:
            page.wait_for_selector("li.new-listing-container", timeout=10000)
        except Exception as e:
            print(f"[WWR] Timeout waiting for job listings: {e}")
            print("[WWR] Dumping first 2000 characters of HTML...")
            print(page.content()[:2000])
            browser.close()
            return []

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    listings = soup.select("li.new-listing-container")
    print(f"[WWR] Found {len(listings)} job <li> elements")

    for li in listings:
        try:
            # THIS is the correct job link
            job_link_tag = li.select_one("a[href^='/remote-jobs/']")
            job_url = f"https://weworkremotely.com{job_link_tag['href']}" if job_link_tag else None

            title_tag = li.select_one("h4.new-listing__header__title")
            company_tag = li.select_one("p.new-listing__company-name")
            region_tag = li.select_one("p.new-listing__company-headquarters")

            if not all([job_url, title_tag, company_tag]):
                continue

            jobs.append({
                "title": title_tag.text.strip(),
                "company": company_tag.text.strip(),
                "region": region_tag.text.strip() if region_tag else "Unknown",
                "url": job_url,
                "source": "weworkremotely"
            })

        except Exception as e:
            print(f"[WWR] Error parsing listing: {e}")
            continue

    print(f"[WWR] scrape_wwr returned {len(jobs)} jobs.")
    return jobs
