import os
import json
from bs4 import BeautifulSoup
from datetime import datetime

def parse_html_bookmarks(file_path, collection_name):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    bookmarks = []
    for link in soup.find_all("a"):
        title = link.get_text(strip=True)
        url = link.get("href")
        add_date = link.get("add_date", None)

        bookmarks.append({
            "id": hash(url),  # simple dedupe key
            "title": title,
            "link": url,
            "created": datetime.utcfromtimestamp(int(add_date)).isoformat() if add_date else "",
            "collection": collection_name,
            "tags": [],
            "summary": None,
            "enriched": False
        })
    return bookmarks

def merge_into_kb(new_entries, kb_file="knowledge.json"):
    try:
        with open(kb_file, "r", encoding="utf-8") as f:
            kb = json.load(f)
    except FileNotFoundError:
        kb = []

    seen = {entry["id"] for entry in kb}
    merged = kb[:]

    for entry in new_entries:
        if entry["id"] not in seen:
            merged.append(entry)

    with open(kb_file, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2)

    print(f"Imported {len(new_entries)} entries, KB now has {len(merged)} total")

if __name__ == "__main__":
    # update these filenames based on your exports
    imports = [
        ("AI.html", "AI"),
        ("VIBEFLOW.html", "Vibeflow")
    ]
    all_entries = []
    for filename, collection in imports:
        if os.path.exists(filename):
            all_entries.extend(parse_html_bookmarks(filename, collection))
        else:
            print(f"⚠️ Skipping {filename}, not found")

    merge_into_kb(all_entries)
