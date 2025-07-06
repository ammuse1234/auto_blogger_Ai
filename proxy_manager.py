import requests
import random
import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# ✅ قائمة الدول الأوروبية المسموح بها
EUROPEAN_COUNTRIES = {
    "fr", "de", "nl", "it", "es", "gb", "pl", "se", "fi", "no", "dk", "be", "at", "ch",
    "ie", "cz", "pt", "sk", "gr", "hu", "ro", "bg", "hr", "ee", "lt", "lv", "si", "cy", "lu"
}

# ⬇️ توليد رابط ديناميكي من الدول الأوروبية
country_param = ",".join(EUROPEAN_COUNTRIES)

# ✅ مصادر البروكسي
PROXY_SOURCES = [
    f"https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=3000&country={country_param}&ssl=all&anonymity=elite",
    "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-List/master/proxy-list.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt"
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
]

BLOG_URL = "https://inspirat12.blogspot.com"

# ✅ اختبار البروكسي مع التحقق من وجود مقالات فعلية + تجربة فتح مقالة مباشرة
def is_proxy_working(proxy, timeout=8):
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    }

    try:
        # الخطوة 1: فتح الصفحة الرئيسية
        response = requests.get(BLOG_URL, proxies=proxies, timeout=timeout)
        if response.status_code != 200:
            return False

        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')

        # الخطوة 2: استخراج روابط المقالات
        article_links = []
        for link in links:
            href = link.get('href')
            if href and href.startswith(BLOG_URL) and href.endswith(".html") and "/search" not in href:
                article_links.append(href)

        if not article_links:
            return False  # لا توجد مقالات صالحة رغم فتح الصفحة

        # الخطوة 3: تجربة فتح أول مقالة للتأكد النهائي
        test_article_url = article_links[0]
        article_response = requests.get(test_article_url, proxies=proxies, timeout=timeout)
        return article_response.status_code == 200

    except:
        return False

# ✅ تحميل البروكسيات من مصدر معين
def fetch_proxies_from_source(source_url):
    try:
        response = requests.get(source_url, timeout=10)
        proxies = response.text.strip().split("\n")
        return [p.strip() for p in proxies if ":" in p]
    except:
        return []

# ✅ تحميل من كل المصادر
def fetch_all_proxies():
    all_proxies = set()
    for url in PROXY_SOURCES:
        proxies = fetch_proxies_from_source(url)
        all_proxies.update(proxies)
    return list(all_proxies)

# ✅ اختبار بالتوازي
def validate_proxies_parallel(proxy_list, max_workers=50):
    valid_proxies = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_proxy = {executor.submit(is_proxy_working, proxy): proxy for proxy in proxy_list}
        for future in as_completed(future_to_proxy):
            proxy = future_to_proxy[future]
            try:
                if future.result():
                    valid_proxies.append(proxy)
            except:
                continue
    return valid_proxies

# ✅ جلب العدد المطلوب من البروكسيات الأوروبية
def get_required_proxies(required_count=50, max_attempts=10):
    all_valid = set()
    attempt = 0

    while len(all_valid) < required_count and attempt < max_attempts:
        print(f"🔄 Attempt {attempt + 1}: Fetching new proxies...")
        raw_proxies = fetch_all_proxies()
        random.shuffle(raw_proxies)
        valid = validate_proxies_parallel(raw_proxies)
        all_valid.update(valid)
        print(f"✅ Found {len(all_valid)} valid proxies so far.")
        attempt += 1
        time.sleep(2)

    if len(all_valid) >= required_count:
        print(f"🎯 Success! Got {required_count} proxies.")
    else:
        print(f"⚠️ Only got {len(all_valid)} proxies after {max_attempts} attempts.")

    return list(all_valid)[:required_count]

def quick_check(proxy, timeout=5):
    try:
        response = requests.get("https://inspirat12.blogspot.com", proxies={
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }, timeout=timeout)
        return response.status_code == 200
    except:
        return False
