import os
from datetime import datetime
from post import post_to_blogger
import openai

# ملفات الذكاء الاصطناعي والترند
from topic_generator import get_trending_topic
from article_generator import generate_article
from utils import is_duplicate, save_posted_title

# ضبط مفتاح OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# استدعاء BLOG_ID من المتغيرات السرية
BLOG_ID = os.getenv("BLOG_ID")

# طباعة معلومات السرية (اختياري للديباغ)
print("🔍 CLIENT_ID:", os.getenv("CLIENT_ID"))
print("🔍 CLIENT_SECRET:", os.getenv("CLIENT_SECRET"))
print("🔍 REFRESH_TOKEN:", os.getenv("REFRESH_TOKEN"))

# تنفيذ النشر
if __name__ == "__main__":
    topic = get_trending_topic()

    if is_duplicate(topic):
        print(f"⏭️ تم تخطي الموضوع المكرر: {topic}")
    else:
        print(f"✍️ توليد مقال عن: {topic}")
        content = generate_article(topic)
        title = f"{topic} ({datetime.now().strftime('%H:%M')})"
        labels = ["Trending", "AI", "News"]

        post_to_blogger(BLOG_ID, title, content, labels)
        save_posted_title(topic)
        print(f"✅ تم النشر: {title}")
