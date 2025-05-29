import datetime
from src.utils.openai_client import call_openai_chat

def enrich_job_row(job):
    prompt = f"""
You are an expert job analyst. Given the job details below, return a JSON object with the following fields:
- cleaned_job_title (string): A cleaner, simplified version of the job title, no brackets or statements about it being remote or the region etc. Just the actual job title. 
- company_summary (string): 200 character summary of what the company does (skip fluff). Look around the web to get a good idea of what the company does, and their culture. 
- job_summary (string): 200 character summary of what the job is (no waffle).
- job_category (string): One of: Engineering, Design, Marketing, Sales, Ops, Product, Leadership, Other.
- estimated_salary (string): Best guess annual, daily or hourly salary range in USD (e.g., "$100–130k/year"). Based on the information you can find, or similar jobs. 
- rarity (integer 1–100): Estimate how rare this job is based on its title, region, estimated salary and description. 1 = very common, 100 = extremely rare. Be strict — only assign scores above 90 if this job is truly unique or highly unusual.

Job Title: {job["job_title"]}
Company: {job["company_name"]}
Region: {job["region"]}
Source: {job["source"]}
Raw Description:
\"\"\"
{job["raw_description"]}
\"\"\"
"""

    result = call_openai_chat(prompt)

    try:
        enriched = result.json() if hasattr(result, "json") else result
        return {
            "cleaned_job_title": enriched["cleaned_job_title"],
            "company_name": job["company_name"],
            "company_summary": enriched["company_summary"],
            "job_summary": enriched["job_summary"],
            "job_URL": job["job_url"],
            "job_category": enriched["job_category"],
            "source": job["source"],
            "region": job["region"],
            "estimated_salary": enriched["estimated_salary"],
            "rarity": enriched["rarity"],
            "created_at": datetime.datetime.utcnow().date().isoformat(),
        }

    except Exception as e:
        print(f"[ENRICH ERROR] Failed to process job: {e}")
        return None
