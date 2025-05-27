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
        page.wait_for_timeout(3000)  # let content load
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    sections = soup.select("section.jobs")  # each job category section

    print(f"[WWR] Found {len(sections)} job sections")

    for section in sections:
        category = section.select_one("h2")
        category_name = category.text.strip() if category else "Unknown"

        listings = section.select("li:not(.view-all)")  # skip 'view all' link
        print(f"[WWR] Found {len(listings)} listings in category '{category_name}'")

        for li in listings:
            try:
                link_tag = li.find("a", href=True)
                if not link_tag:
                    continue
                job_url = "https://weworkremotely.com" + link_tag["href"]

                title_tag = li.find("span", class_="title")
                company_tag = li.find("span", class_="company")
                region_tag = li.find("span", class_="region")

                if not title_tag or not company_tag:
                    continue

                jobs.append({
                    "title": title_tag.text.strip(),
                    "company": company_tag.text.strip(),
                    "region": region_tag.text.strip() if region_tag else "Unknown",
                    "url": job_url,
                    "source": "weworkremotely",
                    "category": category_name
                })

            except Exception as e:
                print(f"[WWR] Error parsing listing: {e}")
                continue

    print(f"[WWR] scrape_wwr returned {len(jobs)} jobs.")
    return jobs
