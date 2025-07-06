import random
import time
from message_generator import generate_message
from mastodon_poster import MastodonPoster
from get_articles import get_articles

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

mastodon = MastodonPoster()

class Agent:
    def __init__(self, proxy):
        self.proxy = proxy

    def simulate_human_behavior(self, url):
        print(f"🌐 Opening browser for: {url}")

        options = uc.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"--proxy-server=http://{self.proxy}")

        try:
            driver = uc.Chrome(optionsoptions, version_main=137)
            driver.get(url)

            # ⏳ وقت التفاعل
            scroll_time = random.uniform(40, 70)
            print(f"🕒 Simulating read time: {int(scroll_time)}s")

            start_time = time.time()
            while time.time() - start_time < scroll_time:
                driver.execute_script("window.scrollBy(0, 200);")
                time.sleep(random.uniform(1, 2))

            print("🧠 Simulating final user interaction...")
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.PAGE_DOWN)

            driver.quit()

        except Exception as e:
            print(f"❌ Browser error on {url}: {e}")
            raise e

    def run(self):
        proxy_str = self.proxy
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
