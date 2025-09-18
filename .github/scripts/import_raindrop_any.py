import os, json, csv
from bs4 import BeautifulSoup

KB_FILE = "knowledge.json"

def load_kb():
    if os.path.exists(KB_FILE):
        with open(KB_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                # Ensure proper shape
                if isinstance(data, dict) and "bookmarks" in data and isinstance(data["bookmarks"], list):
                    return data
                elif isinstance(data, list):
                    return {"bookmarks": data}
                else:
                    return {"bookmarks": []}
            except json.JSONDecodeError:
                return {"bookmarks": []}
    return {"bookmarks": []}

def save_kb(kb):
    with open(KB_FILE, "w", encoding="utf-8") as f:
        json.dump(kb, f, indent=2, ensure_ascii=False)

def parse_html(path):
    bookmarks = []
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        for a in soup.find_all("a"):
            link = a.get("href")
            if link and link.startswith("http"):
                bookmarks.append({
                    "title": a.get_text(strip=True) or link,
                    "link": link,
                    "tags": [],
                    "source_file": os.path.basename(path)
                })
    return bookmarks

def parse_txt(path):
    bookmarks = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("http"):   # only keep valid URLs
                bookmarks.append({
                    "title": line,   # fallback title is URL
                    "link": line,
                    "tags": [],
                    "source_file": os.path.basename(path)
                })
    return bookmarks

def parse_csv(path):
    bookmarks = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            link = row.get("URL") or row.get("url") or row.get("Link")
            if link and link.startswith("http"):
                bookmarks.append({
                    "title": row.get("Title") or row.get("title") or link,
                    "link": link,
                    "tags": row.get("Tags", "").split(",") if "Tags" in row else [],
                    "source_file": os.path.basename(path)
                })
    return bookmarks

if __name__ == "__main__":
    kb = load_kb()

    # Deduplication: by link only
    all_links = { b["link"] for b in kb["bookmarks"] if b.get("link") }

    total_imported = 0
    files_deleted = 0

    for file in os.listdir("."):
        if file.endswith((".html", ".txt", ".csv")):
            print(f"Processing {file}...")
            if file.endswith(".html"):
                new_entries = parse_html(file)
            elif file.endswith(".txt"):
                new_entries = parse_txt(file)
            else:
                new_entries = parse_csv(file)

            imported = 0
            for b in new_entries:
                link = b.get("link")
                if link and link not in all_links:
                    kb["bookmarks"].append(b)
                    all_links.add(link)
                    imported += 1

            total_imported += imported
            print(f"  → Imported {imported} new entries from {file}")

            if os.getenv("CLEANUP", "false").lower() == "true":
                os.remove(file)
                files_deleted += 1
                print(f"  → Deleted {file} after import")

    save_kb(kb)

    print("\n===== Import Summary =====")
    print(f"New entries imported: {total_imported}")
    print(f"Total bookmarks in knowledge.json: {len(kb['bookmarks'])}")
    print(f"Files deleted (CLEANUP=true): {files_deleted}")
    print("==========================\n")
