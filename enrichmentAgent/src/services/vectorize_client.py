import os
import requests

def push_vector_to_cf(vector_id, vector, metadata):
    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{os.environ['CF_VECTORIZE_ACCOUNT_ID']}/vectorize/indexes/"
        f"{os.environ['CF_VECTORIZE_INDEX_NAME']}/vectors"
    )

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

    print("[📡 Sending] Vector to:", url)
    response = requests.post(url, headers=headers, json=payload)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("[⚠️ WARNING] Cloudflare returned an error but continuing:")
        print(e)
        print("[🧾 Response content]:", response.text)

    return response.json()
