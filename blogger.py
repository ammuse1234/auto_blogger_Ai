import requests

def create_post(blog_id, title, content, labels, access_token):
    url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    post_data = {
        "kind": "blogger#post",
        "title": title,
        "content": content,
        "labels": labels
    }
    response = requests.post(url, headers=headers, json=post_data)
    if response.status_code == 200:
        print("✅ Post published successfully!")
        return response.json()
    else:
        print("❌ Failed to publish post:", response.text)
        return None
import json
from auth import get_access_token

def post_to_blogger(blog_id, title, content, labels=[]):
    access_token = get_access_token()

    url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    post = {
        "kind": "blogger#post",
        "blog": {
            "id": blog_id
        },
        "title": title,
        "content": content,
        "labels": labels
    }

    response = requests.post(url, headers=headers, data=json.dumps(post))
    if response.status_code == 200:
        print("✅ Post published successfully!")
    else:
        print("❌ Failed to publish post:", response.text)
