import os

# نقرأ من GitHub secret ونحوله إلى ملف مؤقت
client_secret_content = os.environ.get("GOOGLE_CLIENT_SECRET_JSON")

if client_secret_content:
    with open("client_secret.json", "w") as f:
        f.write(client_secret_content)
        
import random
from post import post_to_blogger
import os
from datetime import datetime

blog_id = os.environ['BLOG_ID']

# 👇 نموذج توليد مقال عشوائي بسيط
def generate_post():
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

    title = random.choice(titles) + f" ({datetime.now().strftime('%H:%M')})"
    content = random.choice(contents)
    return title, content

if __name__ == "__main__":
    title, content = generate_post()
    post_to_blogger(blog_id, title, content)
    import get_trending_topics
from article_generator import generate_article
from blogger import create_post
from create_blog import create_blog

if __name__ == "__main__":
    create_blog()

def main():
    topics = get_trending_topics()
    for topic in topics:
        print(f"🧠 Topic: {topic}")
        article = generate_article(topic)
        post_to_blogger(title=topic, content=article, labels=["AI Generated", "Trending"])

if __name__ == "__main__":
    main()
    
import random
from blogger import post_to_blogger
import os

BLOG_ID = os.getenv("BLOG_ID")

def generate_fake_article():
    titles = ["Top 10 Tech Trends", "Why AI is the Future", "How to Stay Productive"]
    contents = [
        "<p>This is a trending topic about technology.</p>",
        "<p>Artificial Intelligence is growing fast!</p>",
        "<p>Use these tips to stay productive in your work and life.</p>"
    ]
    labels = ["Tech", "AI", "Productivity"]

    index = random.randint(0, len(titles) - 1)
    return titles[index], contents[index], [labels[index]]

if __name__ == "__main__":
    title, content, labels = generate_fake_article()
    post_to_blogger(BLOG_ID, title, content, labels)
