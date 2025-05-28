from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def grab_wwr_description(job_url: str) -> str:
    print(f"\n[DESC] Opening: {job_url}")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_page()
            page.goto(job_url, timeout=60000)

            # Let JS content load
            page.wait_for_timeout(3000)

            html = page.content()
            browser.close()

        soup = BeautifulSoup(html, "html.parser")

        desc_container = soup.select_one("div.lis-container__job__content")

        if not desc_container:
            print("[DESC] ❌ '.lis-container__job__content' not found.")
            print("[DESC] Dumping first 1000 characters of HTML:\n")
            print(html[:1000])
            return "No description found"

        text = desc_container.get_text(separator="\n", strip=True)
        print(f"[DESC] ✅ Extracted {len(text)} characters.")
        return text

    except Exception as e:
        print(f"[DESC] ❗ Error fetching WWR description: {e}")
        return "No description found"
