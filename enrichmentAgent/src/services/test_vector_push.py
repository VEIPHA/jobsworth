import sys
import os
from services.vectorize_client import push_vector_to_cf
import openai
from dotenv import load_dotenv

# Load Railway/Local .env if running locally (optional)
load_dotenv()

# ---- Dummy job data ----
job_id = "test-job-001"
description = "We are hiring a remote product manager to lead AI-driven growth."
title = "Product Manager"
company = "ExampleCo"
url = "https://example.com/jobs/001"

# ---- Generate OpenAI embedding ----
embedding = openai.Embedding.create(
    model="text-embedding-3-small",
    input=description
).data[0].embedding

# ---- Push to Cloudflare Vectorize ----
response = push_vector_to_cf(
    vector_id=job_id,
    vector=embedding,
    metadata={
        "title": title,
        "company": company,
        "url": url
    }
)

print(f"[✅ SUCCESS] Vector pushed for job '{job_id}' at '{url}'")
print(f"[🔁 Cloudflare Response] {response}")
