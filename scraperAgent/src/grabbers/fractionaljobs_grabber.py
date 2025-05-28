from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def grab_fractional_description(job_url: str) -> str:
    print(f"\n[DESC] Opening: {job_url}")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_page()
            page.goto(job_url, timeout=60000)

            # Wait for the actual description container to load
            try:
                page.wait_for_selector(".text-rich-text.w-richtext", timeout=10000)
            except Exception:
                print("[DESC] ❌ Timed out waiting for description container.")
                html = page.content()
                print(html[:1000])
                browser.close()
                return "No description found"

            html = page.content()
            browser.close()

        soup = BeautifulSoup(html, "html.parser")

        # Use correct selector found in DevTools
        desc_container = soup.select_one(".text-rich-text.w-richtext")

        if not desc_container:
            print("[DESC] ❌ '.text-rich-text.w-richtext' not found.")
            print("[DESC] Dumping first 1000 characters of HTML:\n")
            print(html[:1000])
            return "No description found"

        text = desc_container.get_text(separator="\n", strip=True)
        print(f"[DESC] ✅ Extracted {len(text)} characters.")
        return text

    except Exception as e:
        print(f"[DESC] ❗ Error fetching description: {e}")
        return "No description found"
