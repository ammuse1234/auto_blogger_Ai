import os
import requests
from auth import get_authenticated_service

# نحصل على ID المدونة من متغير بيئة
BLOG_ID = os.getenv("BLOG_ID")

def create_blog(name):
    """
    تنشئ مدونة جديدة باسم معين.
    """
    service = get_authenticated_service()
    user = service.users().get(userId='self').execute()

    blog_body = {
        "kind": "blogger#blog",
        "name": name
    }

    try:
        blog = service.blogs().insert(blog=blog_body, isPrivate=True, userId=user["id"]).execute()
        print(f"✅ Created blog: {blog['name']} (ID: {blog['id']})")
        return blog
    except Exception as e:
        print(f"❌ Failed to create blog: {e}")
        return None

def post_to_blogger(title, content, labels=None):
    """
    تنشر مقال في المدونة المحددة بالـ BLOG_ID.
    """
    service = get_authenticated_service()
    if not BLOG_ID:
        print("❌ BLOG_ID is not set in environment variables.")
        return

    try:
        post = {
            "kind": "blogger#post",
            "title": title,
            "content": content,
            "labels": labels or []
        }

        result = service.posts().insert(blogId=BLOG_ID, body=post).execute()
        print(f"✅ Posted: {result['title']} (ID: {result['id']})")
    except Exception as e:
        print(f"❌ Failed to post: {e}")
