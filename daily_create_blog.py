import os
import requests
from datetime import datetime
from auth import get_access_token

def create_blog(title, description, access_token):
    url = "https://www.googleapis.com/blogger/v3/blogs"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {
        "kind": "blogger#blog",
        "name": title,
        "description": description
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        print(f"✅ Blog created: {response.json()['name']}")
        print(f"🆔 Blog ID: {response.json()['id']}")
    else:
        print(f"❌ Failed to create blog: {response.status_code} - {response.text}")

def main():
    # توليد اسم مدونة فريد حسب التاريخ
    today = datetime.now().strftime("%Y-%m-%d")
    blog_title = f"Auto AI Blog - {today}"
    blog_description = "This blog is created automatically using Blogger API and Python."

    access_token = get_access_token()
    create_blog(blog_title, blog_description, access_token)

if __name__ == "__main__":
    main()
