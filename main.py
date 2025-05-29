from trends import get_trending_topics
from article_generator import generate_article
from blogger import post_to_blogger

def main():
    topics = get_trending_topics()
    for topic in topics:
        print(f"🧠 Topic: {topic}")
        article = generate_article(topic)
        post_to_blogger(title=topic, content=article, labels=["AI Generated", "Trending"])

if __name__ == "__main__":
    main()