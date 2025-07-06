import requests
import random
import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# ✅ الدول الأوروبية
EUROPEAN_COUNTRIES = {
    "fr", "de", "nl", "it", "es", "gb", "pl", "se", "fi", "no", "dk", "be", "at", "ch",
    "ie", "cz", "pt", "sk", "gr", "hu", "ro", "bg", "hr", "ee", "lt", "lv", "si", "cy", "lu"
}
country_param = ",".join(EUROPEAN_COUNTRIES)

# ✅ مصادر البروكسي
PROXY_SOURCES = [
    f"https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=3000&country={country_param}&ssl=all&anonymity=elite",
    "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-List/master/proxy-list.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
]

# ✅ رابط مدونتك
BLOG_URL = "https://ammuse12345.blogspot.com"

# ✅ اختبار البروكسي (هل يفتح الصفحة + مقالة حقيقية؟)
def is_proxy_working(proxy, timeout=8):
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    }

    try:
        response = requests.get(BLOG_URL, proxies=proxies, timeout=timeout)
        if response.status_code != 200:
            return False

        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        article_links = [link.get('href') for link in links if link.get('href') and link.get('href').startswith(BLOG_URL) and link.get('href').endswith(".html") and "/search" not in link.get('href')]

        if not article_links:
            return False

        # تجربة فتح مقالة
        test_article = article_links[0]
        article_response = requests.get(test_article, proxies=proxies, timeout=timeout)
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

# ✅ استخراج IP من البروكسي
def extract_ip_from_proxy(proxy_string):
    return proxy_string.split(":")[0].strip()

# ✅ فحص هل البروكسي مشبوه باستخدام ip-api.com
def is_proxy_suspicious(proxy_ip):
    try:
        url = f"http://ip-api.com/json/{proxy_ip}?fields=status,message,query,countryCode,org,as,mobile,proxy,hosting"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data["status"] != "success":
            print(f"⚠️ IP-API failed for {proxy_ip}: {data.get('message')}")
            return True

        if data.get("proxy") or data.get("hosting"):
            print(f"❌ Rejected suspicious IP: {proxy_ip} ({data.get('as')})")
            return True

        return False
    except:
        return True  # نعتبره مشبوه إذا فشل الفحص

# ✅ فحص البروكسيات بالتوازي + استبعاد المشبوه
def validate_proxies_parallel(proxy_list, max_workers=50):
    valid_proxies = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_proxy = {executor.submit(is_proxy_working, proxy): proxy for proxy in proxy_list}

        for future in as_completed(future_to_proxy):
            proxy = future_to_proxy[future]
            try:
                if future.result():
                    ip = extract_ip_from_proxy(proxy)
                    if not is_proxy_suspicious(ip):
                        valid_proxies.append(proxy)
                    else:
                        print(f"⛔ Proxy rejected (bad reputation): {proxy}")
            except:
                continue
    return valid_proxies

# ✅ جلب عدد محدد من البروكسيات النظيفة
def get_required_proxies(required_count=50, max_attempts=10):
    all_valid = set()
    attempt = 0

    while len(all_valid) < required_count and attempt < max_attempts:
        print(f"🔄 Attempt {attempt + 1}: Fetching proxies...")
        raw_proxies = fetch_all_proxies()
        random.shuffle(raw_proxies)
        valid = validate_proxies_parallel(raw_proxies)
        all_valid.update(valid)
        print(f"✅ Valid proxies found: {len(all_valid)}")
        attempt += 1
        time.sleep(2)

    if len(all_valid) >= required_count:
        print(f"🎯 Success! {required_count} proxies ready.")
    else:
        print(f"⚠️ Only {len(all_valid)} proxies after {max_attempts} attempts.")

    return list(all_valid)[:required_count]

# ✅ فحص سريع (للطوارئ)
def quick_check(proxy, timeout=5):
    try:
        response = requests.get(BLOG_URL, proxies={
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }, timeout=timeout)
        return response.status_code == 200
    except:
        return False
