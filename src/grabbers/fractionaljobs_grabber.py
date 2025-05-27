from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def grab_fractional_description(job_url: str) -> str:
    print(f"\n[DESC] Opening: {job_url}")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_page()
            page.goto(job_url, timeout=60000)

            # Give JS time to run
            page.wait_for_timeout(3000)

            # Optional: take a screenshot to inspect what's rendered
            page.screenshot(path="fractional_debug.png", full_page=True)

            html = page.content()
            browser.close()

        soup = BeautifulSoup(html, "html.parser")

        # Save full HTML for inspection
        with open("fractional_debug.html", "w", encoding="utf-8") as f:
            f.write(html)

        # Corrected selector based on real HTML
        desc_container = soup.select_one("div.job-description")

        if not desc_container:
            print("[DESC] ❌ 'div.job-description' not found.")
            print("[DESC] Dumping first 1000 characters of HTML:\n")
            print(html[:1000])
            return "No description found"

        text = desc_container.get_text(separator="\n", strip=True)
        print(f"[DESC] ✅ Extracted {len(text)} characters.")
        return text

    except Exception as e:
        print(f"[DESC] ❗ Error fetching description: {e}")
        return "No description found"
