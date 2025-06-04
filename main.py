import os
from datetime import datetime
from post import post_to_blogger
from topic_generator import get_trending_topic
from article_generator import generate_article
from utils import is_duplicate, save_posted_title

# تأكد من ضبط مفتاح API الخاص بـ OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# معرف المدونة
BLOG_ID = os.getenv("BLOG_ID")

print("🔍 CLIENT_ID:", os.getenv("CLIENT_ID"))
print("🔍 CLIENT_SECRET:", os.getenv("CLIENT_SECRET"))
print("🔍 REFRESH_TOKEN:", os.getenv("REFRESH_TOKEN"))

if __name__ == "__main__":
    try:
        topic = get_trending_topic()
    except Exception as e:
        print("Error fetching Google Trends:", e)
        topic = "Latest news updates"

    if is_duplicate(topic):
        print(f"⏭️ تم تخطي الموضوع المكرر: {topic}")
    else:
        print(f"✍️ توليد مقال عن: {topic}")
        try:
            content = generate_article(topic)
        except Exception as e:
            print("❌ خطأ في توليد المقال:", e)
            content = "This is a default article content due to error in generating article."

        title = f"{topic} ({datetime.now().strftime('%H:%M')})"
        labels = ["Trending", "AI", "News"]

        try:
            post_to_blogger(BLOG_ID, title, content, labels)
            save_posted_title(topic)
            print(f"✅ تم النشر: {title}")
        except Exception as e:
            print("❌ خطأ في النشر على Blogger:", e)
