import json
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTED_FILE_PATH = os.path.join(BASE_DIR, "posted_articles.json")

def normalize_title(title: str) -> str:
    title = title.lower().strip()
    title = re.sub(r"[^\w\s]", "", title)
    title = re.sub(r"\s+", " ", title)
    return title

def load_posted_titles():
    if os.path.exists(POSTED_FILE_PATH):
        with open(POSTED_FILE_PATH, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_posted_title(title):
    posted = load_posted_titles()
    normalized_title = normalize_title(title)
    if normalized_title not in posted:
        posted.append(normalized_title)
        with open(POSTED_FILE_PATH, "w") as file:
            json.dump(posted, file, ensure_ascii=False, indent=2)

def is_duplicate(title):
    normalized_title = normalize_title(title)
    return normalized_title in load_posted_titles()
