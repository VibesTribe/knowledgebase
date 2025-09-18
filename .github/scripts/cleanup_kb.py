import os, json

KB_FILE = "knowledge.json"

def load_kb():
    if os.path.exists(KB_FILE):
        with open(KB_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, dict) and "bookmarks" in data:
                    return data
                elif isinstance(data, list):
                    return {"bookmarks": data}
            except json.JSONDecodeError:
                pass
    return {"bookmarks": []}

def save_kb(kb):
    with open(KB_FILE, "w", encoding="utf-8") as f:
        json.dump(kb, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    kb = load_kb()
    bookmarks = kb.get("bookmarks", [])

    print(f"Original total: {len(bookmarks)}")

    seen = set()
    cleaned = []
    removed = 0

    for b in bookmarks:
        link = b.get("link")
        if link and link not in seen:
            cleaned.append(b)
            seen.add(link)
        else:
            removed += 1

    kb["bookmarks"] = cleaned
    save_kb(kb)

    print("\n===== Cleanup Summary =====")
    print(f"Original entries: {len(bookmarks)}")
    print(f"Duplicates removed: {removed}")
    print(f"Final total: {len(cleaned)}")
    print("===========================")
