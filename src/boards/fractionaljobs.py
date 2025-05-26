import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def scrape_fractionaljobs():
    url = "https://www.fractionaljobs.io/#jobs"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"[ERROR] Failed to fetch page: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Look for the actual job items in the HTML structure
    job_items = soup.select(".job-item")
    jobs = []

    print(f"Found {len(job_items)} job elements")

    for job in job_items:
        try:
            # Extract job title and company from job-item_name_url
            name_url_block = job.select_one(".job-item_name_url")
            if not name_url_block:
                continue

            # Get all h3 elements which contain company and title
            h3_elements = name_url_block.select("h3.text-size-regular.text-inline")
            if len(h3_elements) < 3:
                continue
            
            company = h3_elements[0].get_text(strip=True)
            title = h3_elements[2].get_text(strip=True)
            
            # Extract URL from the link
            job_link = job.select_one(".job-item_link-to-job")
            if job_link and job_link.get('href'):
                job_url = job_link['href']
                # Convert relative URL to absolute URL
                if job_url.startswith('/'):
                    job_url = "https://www.fractionaljobs.io" + job_url
                elif not job_url.startswith('http'):
                    job_url = "https://www.fractionaljobs.io/" + job_url
            else:
                # Try to get URL from company link
                company_link = job.select_one(".job-item_company-link")
                if company_link and company_link.get('href'):
                    job_url = company_link['href']
                    # Convert relative URL to absolute URL
                    if job_url.startswith('/'):
                        job_url = "https://www.fractionaljobs.io" + job_url
                    elif not job_url.startswith('http'):
                        job_url = "https://www.fractionaljobs.io/" + job_url
                else:
                    job_url = "https://www.fractionaljobs.io/#jobs"

            # Extract additional job info (hours, pay, location)
            more_info_block = job.select_one(".job-item_more-info")
            region = "Remote"  # Default
            if more_info_block:
                info_text = more_info_block.get_text(" ", strip=True)
                # Try to extract location from the info text
                # Usually formatted like "10 - 20 hrs | $80K - $100K | Remote"
                parts = info_text.split("|")
                if len(parts) >= 3:
                    region = parts[-1].strip()
                elif len(parts) >= 2:
                    region = parts[-1].strip()

            # Skip if we couldn't extract basic info
            if not company or not title:
                continue

            jobs.append({
                "title": title,
                "company": company,
                "region": region,
                "url": job_url,
                "source": "fractionaljobs",
                "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            })

        except Exception as e:
            print(f"[ERROR] Error parsing job item: {e}")
            continue

    print(f"[INFO] Scraped {len(jobs)} jobs from fractionaljobs.io")
    return jobs

