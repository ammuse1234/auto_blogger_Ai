import os
import requests
from auth import get_authenticated_service 

BLOG_ID = os.getenv("BLOG_ID")

def post_to_blogger(title, content, labels=None):
    service = get_authenticated_service()
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "kind": "blogger#post",
        "title": title,
        "content": content,
        "labels": labels or []
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"✅ Posted: {title}")
    else:
        print(f"❌ Failed to post: {response.text}")
