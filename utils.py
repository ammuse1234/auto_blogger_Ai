import json
import os

def load_posted_titles():
    if os.path.exists("posted_articles.json"):
        with open("posted_articles.json", "r") as file:
            return json.load(file)
    return []

def save_posted_title(title):
    posted = load_posted_titles()
    posted.append(title)
    with open("posted_articles.json", "w") as file:
        json.dump(posted, file)

def is_duplicate(title):
    return title in load_posted_titles()
