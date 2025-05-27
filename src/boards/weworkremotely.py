from playwright.sync_api import sync_playwright

def scrape_wwr():
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://weworkremotely.com/")
        content = page.content()
        browser.close()

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")
    listings = soup.select("li.new-listing-container")
    print(f"Found {len(listings)} job <li> elements")

    for li in listings:
        link_tag = li.find("a", href=True)
        if not link_tag:
            continue

        job_url = "https://weworkremotely.com" + link_tag["href"]
        title_tag = li.find("h4", class_="new-listing__header__title")
        company_tag = li.find("p", class_="new-listing__company-name")
        location_tag = li.find("p", class_="new-listing__company-headquarters")

        if not title_tag or not company_tag:
            continue

        jobs.append({
            "title": title_tag.text.strip(),
            "company": company_tag.text.strip(),
            "region": location_tag.text.strip() if location_tag else "Unknown",
            "url": job_url,
            "source": "weworkremotely"
        })

    print(f"scrape_wwr returned {len(jobs)} jobs.")
    return jobs
