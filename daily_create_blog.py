import os
from datetime import datetime
from auth import get_access_token
import requests

def post_welcome_article(blog_id, access_token, date_label):
    url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    title = f"Welcome - {date_label}"
    content = f"<p>This is the daily start post for {date_label}. Stay tuned for more updates throughout the day!</p>"
    labels = [date_label]

    data = {
        "kind": "blogger#post",
        "title": title,
        "content": content,
        "labels": labels
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        post = response.json()
        print(f"✅ Welcome post published: {post['title']} | ID: {post['id']}")
    else:
        print(f"❌ Failed to publish welcome post: {response.status_code} - {response.text}")

def main():
    blog_id = os.environ.get("BLOG_ID")
    if not blog_id:
        raise Exception("❌ BLOG_ID is not set in environment variables.")
    
    access_token = get_access_token()
    today = datetime.now().strftime("%Y-%m-%d")
    post_welcome_article(blog_id, access_token, today)

if __name__ == "__main__":
    main()
