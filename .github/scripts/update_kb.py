import os, requests

ACCESS_TOKEN = os.getenv("RAINDROP_ACCESS_TOKEN")

def fetch_bookmarks():
    url = "https://api.raindrop.io/rest/v1/raindrops/0"  # all collections
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    resp = requests.get(url, headers=headers)
    print("Status code:", resp.status_code)
    print("Raw response (first 200 chars):", resp.text[:200])
    resp.raise_for_status()
    return resp.json()["items"]

if __name__ == "__main__":
    print(">>> DEBUG: Running safe fetch (no params) <<<")
    bookmarks = fetch_bookmarks()
    print("Fetched bookmarks:")
    for b in bookmarks[:5]:  # just show first 5
        print("-", b["title"])
        print("   Link:", b["link"])
        print("   Collection ID:", b.get("collectionId"))
        print("   Created:", b["created"])
