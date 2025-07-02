import random
import time
import requests
from message_generator import generate_message
from get_articles import get_articles
from bs4 import BeautifulSoup
import proxy_manager2 # ملف إدارة البروكسيات


class Agent:
    def __init__(self, proxy_str):
        self.proxy_str = proxy_str
        self.set_proxy(proxy_str)

    def set_proxy(self, proxy_str):
        self.proxy_str = proxy_str
        self.proxy = {
            "http": f"http://{proxy_str}",
            "https": f"http://{proxy_str}",
        }
        print(f"🟢 Using proxy: {proxy_str}")

    def replace_proxy(self):
        print(f"🔁 Replacing proxy: {self.proxy_str}")
        proxy_manager.report_failure(self.proxy_str)

        new_proxy = proxy_manager.replace_proxy(self.proxy_str, used_proxies=set())
        if not new_proxy:
            print("❌ No proxies left to replace, stopping agent.")
            raise Exception("No proxies left")
        self.set_proxy(new_proxy)

    def simulate_human_behavior(self, url):
        print(f"👀 Visiting: {url}")
        while True:
            try:
                response = requests.get(url, proxies=self.proxy, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')

                scroll_time = random.uniform(5, 12)
                print(f"🕒 Simulating read time: {int(scroll_time)}s")
                time.sleep(scroll_time)

                print("🧠 Simulating user interaction...")
                time.sleep(random.uniform(1, 3))

                break  # نجاح، نخرج من اللوب

            except Exception as e:
                err_str = str(e)
                print(f"❌ Failed on {url}: {err_str}")

                error_keywords = [
                    "timeout", "connectionerror", "connectionreseterror",
                    "proxyerror", "readtimeout", "remotedisconnected",
                    "failed to establish a new connection", "connection aborted",
                    "max retries exceeded"
                ]
                if any(keyword in err_str.lower() for keyword in error_keywords):
                    print(f"⚠️ Detected proxy issue, replacing proxy...")
                    proxy_manager.report_failure(self.proxy_str)
                    new_proxy = proxy_manager.replace_proxy(self.proxy_str, set())
                    if new_proxy:
                        self.set_proxy(new_proxy)
                        print(f"🟢 Switched to new proxy: {new_proxy}")
                        continue  # نعيد المحاولة مع البروكسي الجديد
                    else:
                        print("❌ No proxies left to switch, aborting.")
                        raise e
                else:
                    raise e

    def run(self):
        while True:
            try:
                articles = None
                while articles is None or len(articles) == 0:
                    try:
                        articles = get_articles(self.proxy_str)
                    except Exception as e:
                        print(f"❌ Error getting articles: {e}")
                        self.replace_proxy()
                        articles = None
                    if articles is None or len(articles) == 0:
                        print("⚠️ No articles found, retrying in 30s...")
                        time.sleep(30)

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
                        self.replace_proxy()
                        break  # نوقف الحلقة الحالية ونبدأ من جديد بالبروكسي الجديد

            except Exception as e:
                print(f"❌ Critical error in run loop: {e}")
                self.replace_proxy()
