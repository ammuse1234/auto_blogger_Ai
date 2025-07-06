import requests
from bs4 import BeautifulSoup

BLOG_URL = "https://inspirat12.blogspot.com"

def is_proxy_working(proxy):
    """
    يتحقق مما إذا كان البروكسي يعمل فعلاً عن طريق الوصول للمدونة
    والتأكد من وجود مقالات (تنتهي بـ .html).
    """
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    }
    try:
        response = requests.get(BLOG_URL, proxies=proxies, timeout=8)
        if response.status_code != 200:
            return False

        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')

        # نتحقق من وجود روابط مقالات
        for link in links:
            href = link.get('href')
            if (
              href and
              href.startswith(BLOG_URL) and
              ".html" in href and
              "/search" not in href and
              "#comments" not in href
               ):
                return True  # ✅ البروكسي يفتح المدونة ويوجد مقالات
        return False  # ❌ لا توجد مقالات رغم فتح الصفحة
    except:
        return False

def get_articles(proxy):
    """
    يجلب روابط المقالات من مدونة بلوجر باستخدام بروكسي محدد.
    """
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    }

    try:
        response = requests.get(BLOG_URL, proxies=proxies, timeout=17)
        if response.status_code != 200:
            print(f"⚠️ Failed to fetch blog: Status {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')

        articles = []
        for link in links:
            href = link.get('href')
            if (
                href and
                href.startswith(BLOG_URL) and
                ".html" in href and
                "/search" not in href
            ):
                articles.append(href)

        # إزالة التكرار
        articles = list(set(articles))

        print(f"✅ Found {len(articles)} articles.")
        return articles

    except Exception as e:
        print(f"❌ Error fetching articles with proxy {proxy}: {e}")
        return []
