import random
import time
import requests
from message_generator import generate_message
from mastodon_poster import MastodonPoster
from get_articles import get_articles
from bs4 import BeautifulSoup

mastodon = MastodonPoster()

class Agent:
    def __init__(self, proxy):
        self.proxy = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }

    def simulate_human_behavior(self, url):
        print(f"👀 Visiting: {url}")
        try:
            response = requests.get(url, proxies=self.proxy, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            scroll_time = random.uniform(40, 70)
            print(f"🕒 Simulating read time: {int(scroll_time)}s")
            time.sleep(scroll_time)

            print("🧠 Simulating user interaction...")
            time.sleep(random.uniform(1, 3))

        except Exception as e:
            print(f"❌ Failed to simulate behavior on {url}: {e}")
            raise e

    def run(self):
        proxy_str = self.proxy["http"].replace("http://", "")
        articles = get_articles(proxy_str)
        if not articles:
            print("⚠️ No articles found.")
            return

        selected_articles = random.sample(articles, min(len(articles), random.randint(3, 5)))

        for article_url in selected_articles:
            try:
                self.simulate_human_behavior(article_url)

                message = generate_message(article_url)
                print(f"📝 Message: {message}")

                print("🐘 Posting to Mastodon...")
                success = mastodon.post(message, article_url)
                if not success:
                    print("⚠️ Failed to post to Mastodon.")

                time.sleep(random.randint(8, 15))

            except Exception as e:
                print(f"❌ Error handling article {article_url}: {e}")
