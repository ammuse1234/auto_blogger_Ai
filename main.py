import os

# نقرأ من GitHub secret ونحوله إلى ملف مؤقت
client_secret_content = os.environ.get("GOOGLE_CLIENT_SECRET_JSON")

if client_secret_content:
    with open("client_secret.json", "w") as f:
        f.write(client_secret_content)
        
from trends import get_trending_topics
from article_generator import generate_article
from blogger import create_post

def main():
    topics = get_trending_topics()
    for topic in topics:
        print(f"🧠 Topic: {topic}")
        article = generate_article(topic)
        post_to_blogger(title=topic, content=article, labels=["AI Generated", "Trending"])

if __name__ == "__main__":
    main()
