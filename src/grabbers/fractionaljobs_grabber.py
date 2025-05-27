from playwright.sync_api import sync_playwright

def grab_fractional_description(job_url: str) -> str:
    print(f"[DESC] Opening {job_url}")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_page()
            page.goto(job_url, timeout=60000)
            page.wait_for_timeout(3000)  # Wait for JS content

            # Try grabbing rendered description
            html = page.content()
            browser.close()

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        desc_container = soup.select_one("div[data-controller='job-description']")

        if not desc_container:
            print(f"[DESC] No description found in page HTML.")
            return ""

        return desc_container.get_text(separator="\n", strip=True)

    except Exception as e:
        print(f"[DESC] Error fetching {job_url}: {e}")
        return ""
