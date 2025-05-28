from playwright.sync_api import sync_playwright

def grab_wwr_description(job_url: str) -> str:
    print(f"\n[DESC] Opening: {job_url}")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            context = browser.new_context(user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            ))
            page = context.new_page()

            page.goto(job_url, timeout=60000)
            page.wait_for_selector("div.lis-container__job__content", timeout=10000)
            page.wait_for_timeout(1000)  # slight buffer after selector appears

            text = page.locator("div.lis-container__job__content").nth(0).inner_text()
            print(f"[DESC] ✅ Extracted {len(text)} characters.")
            return text

    except Exception as e:
        print(f"[DESC] ❗ Error fetching WWR description: {e}")
        return "No description found"
