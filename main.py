import os
import random
from datetime import datetime
from post import post_to_blogger
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
# استدعاء BLOG_ID من المتغيرات السرية
BLOG_ID = os.getenv("BLOG_ID")

# توليد مقال وهمي من مجموعة
def generate_fake_article():
    titles = [
        "Top AI Tools for 2025",
        "How to Stay Productive with Automation",
        "Trending Topics This Week",
        "Simple Guide to Blogging with AI",
        "The Future of Content Creation"
    ]
    contents = [
        "<p>Welcome to today’s post! We explore how AI is changing the content landscape.</p>",
        "<p>This blog is powered by automation! Here are the benefits...</p>",
        "<p>Here are the top 5 trends right now:</p><ul><li>AI</li><li>Automation</li><li>SEO</li></ul>",
        "<p>Blogging has never been easier. Thanks to Python and Google APIs!</p>",
        "<p>AI is not just the future, it's now. Let's explore how...</p>"
    ]
    labels = ["AI", "Automation", "Trends", "Guide", "Future"]

    index = random.randint(0, len(titles) - 1)
    title = titles[index] + f" ({datetime.now().strftime('%H:%M')})"
    content = contents[index]
    labels = [labels[index]]

    return title, content, labels

# تنفيذ النشر
if __name__ == "__main__":
    title, content, labels = generate_fake_article()
    post_to_blogger(BLOG_ID, title, content, labels)
