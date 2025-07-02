from mastodon import Mastodon
import os
import time
import random

class MastodonPoster:
    def __init__(self):
        self.api_base_url = os.getenv("MASTODON_API_BASE_URL")  # مثلاً https://mastodon.social
        self.access_token = os.getenv("MASTODON_ACCESS_TOKEN")

        if not self.api_base_url or not self.access_token:
            raise ValueError("Missing Mastodon API_BASE_URL or ACCESS_TOKEN environment variables.")

        self.mastodon = Mastodon(
            access_token=self.access_token,
            api_base_url=self.api_base_url
        )

    def post(self, message, url=None):
        try:
            # دمج الرابط مع الرسالة لو موجود
            status = message
            if url:
                status += f" {url}"

            # تأخير عشوائي لتقليل الحظر
            time.sleep(random.uniform(5, 15))

            self.mastodon.status_post(status)
            print(f"✅ Successfully posted to Mastodon: {status[:50]}...")
            return True
        except Exception as e:
            print(f"❌ Failed to post on Mastodon: {e}")
            return False
