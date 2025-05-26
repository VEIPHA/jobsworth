import requests
from bs4 import BeautifulSoup

def scrape_wwr():
    url = "https://weworkremotely.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    listings = soup.select("li.new-listing-container")

    print(f"Found {len(listings)} job <li> elements")

    jobs = []

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
