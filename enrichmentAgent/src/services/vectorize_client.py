import os
import requests

def push_vector_to_cf(vector_id, vector, metadata):
    url = f"https://api.cloudflare.com/client/v4/accounts/{os.environ['CF_VECTORIZE_ACCOUNT_ID']}/ai/vectorize/indexes/{os.environ['CF_VECTORIZER_INDEX_NAME']}/vectors"
    headers = {
        "Authorization": f"Bearer {os.environ['CF_VECTORIZE_API_KEY']}",
        "Content-Type": "application/json"
    }
    payload = {
        "vectors": [{
            "id": str(vector_id),
            "values": vector,
            "metadata": metadata
        }]
    }
    print("[DEBUG] URL:", url)
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()
