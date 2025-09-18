import os, json
from bs4 import BeautifulSoup

KB_FILE = "knowledge.json"

def load_kb():
    if os.path.exists(KB_FILE):
        with open(KB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"bookmarks": []}

def save_kb(kb):
    with open(KB_FILE, "w", encoding="utf-8") as f:
        json.dump(kb, f, indent=2, ensure_ascii=False)

def parse_html(path):
    bookmarks = []
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        for a in soup.find_all("a"):
            bookmarks.append({
                "title": a.get_text(strip=True),
                "link": a.get("href"),
                "tags": [],
                "source_file": os.path.basename(path)
            })
    return bookmarks

if __name__ == "__main__":
    kb = load_kb()
    all_bookmarks = { (b["title"], b["link"]) for b in kb["bookmarks"] }

    total_imported = 0
    files_deleted = 0

    for file in os.listdir("."):
        if file.endswith(".html"):
            print(f"Processing {file}...")
            new_entries = parse_html(file)

            imported = 0
            for b in new_entries:
                key = (b["title"], b["link"])
                if key not in all_bookmarks:
                    kb["bookmarks"].append(b)
                    all_bookmarks.add(key)
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
