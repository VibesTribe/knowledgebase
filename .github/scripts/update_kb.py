print(">>> DEBUG: Script is running the NEW version <<<")

import os, requests

ACCESS_TOKEN = os.getenv("RAINDROP_ACCESS_TOKEN")

def fetch_bookmarks():
    url = "https://api.raindrop.io/rest/v1/raindrops/0"
    params = {"perpage": 5, "page": 0, "sort": "created"}  # ✅ safe params
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    resp = requests.get(url, headers=headers, params=params)
    print("Status code:", resp.status_code)  # debug
    print("Raw response:", resp.text[:200])  # preview first 200 chars
    resp.raise_for_status()
    return resp.json()["items"]

if __name__ == "__main__":
    bookmarks = fetch_bookmarks()
    print("Fetched bookmarks:")
    for b in bookmarks:
        print("-", b["title"], b["link"])
