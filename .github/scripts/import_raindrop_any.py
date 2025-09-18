import os
import json
import csv
from bs4 import BeautifulSoup
from datetime import datetime

def parse_html(file_path, collection):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    bookmarks = []
    for link in soup.find_all("a"):
        title = link.get_text(strip=True)
        url = link.get("href")
        add_date = link.get("add_date", None)

        bookmarks.append({
            "id": hash(url),
            "title": title,
            "link": url,
            "created": datetime.utcfromtimestamp(int(add_date)).isoformat() if add_date else "",
            "collection": collection,
            "tags": [],
            "summary": None,
            "enriched": False
        })
    return bookmarks

def parse_txt(file_path, collection):
    bookmarks = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(" ", 1)
            if len(parts) == 2:
                url, title = parts
            else:
                url, title = parts[0], ""
            bookmarks.append({
                "id": hash(url),
                "title": title,
                "link": url,
                "created": "",
                "collection": collection,
                "tags": [],
                "summary": None,
                "enriched": False
            })
    return bookmarks

def parse_csv(file_path, collection):
    bookmarks = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = row.get("URL") or row.get("Link") or ""
            title = row.get("Title") or ""
            created = row.get("Created") or ""
            bookmarks.append({
                "id": hash(url),
                "title": title,
                "link": url,
                "created": created,
                "collection": collection,
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
    all_entries = []

    for file in os.listdir("."):
        if file.lower().endswith(".html"):
            all_entries.extend(parse_html(file, os.path.splitext(file)[0]))
        elif file.lower().endswith(".txt"):
            all_entries.extend(parse_txt(file, os.path.splitext(file)[0]))
        elif file.lower().endswith(".csv"):
            all_entries.extend(parse_csv(file, os.path.splitext(file)[0]))

    if not all_entries:
        print("⚠️ No supported files found in repo root")
    else:
        merge_into_kb(all_entries)
