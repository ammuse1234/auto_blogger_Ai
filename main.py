import os
from auth import get_access_token
from blogger import post_to_blogger
from content_generator import generate_article
from google_trends import get_trending_topics
from daily_create_blog import create_blog
# احصل على blog_id من Secrets
BLOG_ID = os.environ.get("BLOG_ID")

def main():
    # احصل على التوكن
    access_token = get_access_token()

    # جلب المواضيع الرائجة
    topics = get_trending_topics()

    if topics:
        for topic in topics[:1]:  # انشر مقال واحد فقط (يمكنك إزالة [:1] إذا تريد الكل)
            title, content = generate_article(topic)
            post_to_blogger(BLOG_ID, title, content, access_token)
            print(f"✅ تم النشر: {title}")
    else:
        print("❌ لا توجد مواضيع تريند حالياً.")

if __name__ == "__main__":
    main()
