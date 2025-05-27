def scrape_fractionaljobs():
    print("[FJ] Starting scrape...")

    url = "https://www.fractionaljobs.io/#jobs"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    print(f"[FJ] Status code: {response.status_code}")
    if response.status_code != 200:
        print(f"[FJ] Failed to fetch page: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    job_items = soup.select(".job-item")
    print(f"[FJ] Found {len(job_items)} job elements")

    jobs = []
    for job in job_items:
        title_block = job.select_one(".job-item_name_url")
        if not title_block:
            continue

        raw_text = title_block.get_text(" ", strip=True)
        raw_text = raw_text.replace("Â", "").strip()

        # Extract job URL
        url_match = re.search(r"\(\s*(http.*?)[\s]*\)", raw_text)
        job_url = url_match.group(1).strip() if url_match else "https://www.fractionaljobs.io/#jobs"

        cleaned_text = re.sub(r"\(\s*http.*?[\s]*\)", "", raw_text).strip()

        if " - " in cleaned_text:
            parts = cleaned_text.split(" - ", 1)
        elif " – " in cleaned_text:
            parts = cleaned_text.split(" – ", 1)
        else:
            parts = ["Unknown", cleaned_text]

        company = parts[0].strip()
        title = parts[1].strip() if len(parts) > 1 else parts[0].strip()

        jobs.append({
            "source": "fractionaljobs",
            "title": title,
            "company": company,
            "location": "Remote",
            "url": job_url
        })

    print(f"[FJ] scrape_fractionaljobs returned {len(jobs)} jobs.")
    return jobs
