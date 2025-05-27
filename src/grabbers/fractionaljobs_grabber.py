import requests
from bs4 import BeautifulSoup

def grab_fractional_description(job_url: str) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(job_url, headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"[DESC] Failed to fetch page: {response.status_code}")
            return ""

        soup = BeautifulSoup(response.text, "html.parser")

        # Adjust the selector if this doesn't return enough
        desc_container = soup.select_one(".job-item_details")
        if not desc_container:
            print(f"[DESC] No job description found at {job_url}")
            return ""

        return desc_container.get_text(separator="\n", strip=True)

    except Exception as e:
        print(f"[DESC] Error grabbing description from {job_url}: {e}")
        return ""
