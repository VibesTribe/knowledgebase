import os, json, requests
from datetime import datetime

ACCESS_TOKEN = os.getenv("RAINDROP_ACCESS_TOKEN")

def fetch_bookmarks():
    url = "https://api.raindrop.io/rest/v1/raindrops/0"
    params = {"perpage": 5, "sort": "-created"}
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()["items"]

def load_kb():
    try:
        with open("knowledge.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_kb(data):
    with open("knowledge.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    kb = load_kb()
    seen_ids = {item["id"] for item in kb}

    new_items = []
    for item in fetch_bookmarks():
        if item["_id"] not in seen_ids:
            new_entry = {
                "id": item["_id"],
                "title": item["title"],
                "link": item["link"],
                "created": item["created"],
                "collection": str(item["collection"]["$id"]),
                "tags": [],
                "summary": None,
                "enriched": False
            }
            kb.append(new_entry)
            new_items.append(new_entry)

    if new_items:
        print(f"Added {len(new_items)} new bookmarks")
    else:
        print("No new bookmarks found")

    save_kb(kb)
