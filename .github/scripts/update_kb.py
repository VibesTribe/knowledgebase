import os
import json
import requests
from datetime import datetime

ACCESS_TOKEN = os.getenv("RAINDROP_ACCESS_TOKEN")

def fetch_bookmarks():
    """Fetch latest bookmarks from Raindrop.io"""
    url = "https://api.raindrop.io/rest/v1/raindrops/0"  # all collections
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    resp = requests.get(url, headers=headers)
    print("Status code:", resp.status_code)
    print("Raw response (first 200 chars):", resp.text[:200])
    resp.raise_for_status()
    return resp.json().get("items", [])

def load_kb():
    """Load existing knowledge.json or start fresh"""
    try:
        with open("knowledge.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_kb(data):
    """Save updated knowledge.json"""
    with open("knowledge.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    try:
        print(">>> Running KB update script <<<")
        bookmarks = fetch_bookmarks()
        kb = load_kb()
        seen_ids = {item["id"] for item in kb}

        new_entries = []
        for b in bookmarks:
            if b["_id"] not in seen_ids:
                entry = {
                    "id": b["_id"],
                    "title": b.get("title", ""),
                    "link": b.get("link", ""),
                    "created": b.get("created", ""),
                    "collection": str(b.get("collectionId", "")),
                    "tags": [],
                    "summary": None,
                    "enriched": False
                }
                kb.append(entry)
                new_entries.append(entry)

        if new_entries:
            print(f"Added {len(new_entries)} new bookmarks")
            save_kb(kb)
        else:
            print("No new bookmarks to add")

    except Exception as e:
        print("ERROR: Could not update KB:", str(e))
