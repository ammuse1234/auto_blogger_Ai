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
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
]

BLOG_URL = "https://ammuse12345.blogspot.com"
MAX_DURATION = 600  # مدة تشغيل السكربت المطلوبة بالثواني (مثلاً 10 دقائق)

# --- قاعدة بيانات البروكسيات (مخزن الإحصائيات) ---
proxy_db = {}

# --- تحديث إحصائيات البروكسي بعد كل عملية ---
def update_proxy_stats(proxy, success, runtime):
    if proxy not in proxy_db:
        proxy_db[proxy] = {
            "success_count": 0,
            "fail_count": 0,
            "avg_runtime": 0.0,
            "currently_used_by": 0,
        }
    info = proxy_db[proxy]
    if success:
        info["success_count"] += 1
        prev_avg = info["avg_runtime"]
        info["avg_runtime"] = (prev_avg * (info["success_count"] - 1) + runtime) / info["success_count"]
    else:
        info["fail_count"] += 1

# --- دالة لاختبار البروكسي مع فتح الصفحة والمقالات ---
def is_proxy_working(proxy, timeout=8):
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    }
    start_time = time.time()
    try:
        # فتح الصفحة الرئيسية للمدونة
        response = requests.get(BLOG_URL, proxies=proxies, timeout=timeout)
        if response.status_code != 200:
            raise Exception("Main page load failed")

        soup = BeautifulSoup(response.text, 'html.parser')
        article_links = [
            link.get('href') for link in soup.find_all('a')
            if link.get('href') and link.get('href').startswith(BLOG_URL) and link.get('href').endswith(".html") and "/search" not in link.get('href')
        ]

        if not article_links:
            raise Exception("No article links found")

        # اختبار فتح أول مقالة
        article_response = requests.get(article_links[0], proxies=proxies, timeout=timeout)
        if article_response.status_code != 200:
            raise Exception("Article page load failed")

        duration = time.time() - start_time
        update_proxy_stats(proxy, success=True, runtime=duration)
        return True
    except Exception:
        update_proxy_stats(proxy, success=False, runtime=0)
        return False

# --- تحميل البروكسيات من مصدر واحد ---
def fetch_proxies_from_source(source_url):
    try:
        response = requests.get(source_url, timeout=10)
        proxies = response.text.strip().split("\n")
        return [p.strip() for p in proxies if ":" in p]
    except:
        return []

# --- تحميل البروكسيات من كل المصادر ---
def fetch_all_proxies():
    all_proxies = set()
    for url in PROXY_SOURCES:
        proxies = fetch_proxies_from_source(url)
        all_proxies.update(proxies)
    return list(all_proxies)

# --- اختبار البروكسيات بالتوازي ---
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

# --- حساب تقييم تحمل البروكسي ---
def calculate_endurance_score(proxy_info, expected_duration=MAX_DURATION):
    success = proxy_info.get("success_count", 0)
    fail = proxy_info.get("fail_count", 0)
    used = proxy_info.get("currently_used_by", 0)
    avg_runtime = proxy_info.get("avg_runtime", expected_duration / 2)

    total = success + fail
    success_ratio = success / total if total > 0 else 0.5
    runtime_factor = min(avg_runtime / expected_duration, 2.0)
    usage_penalty = used * 5

    score = (success_ratio * 100 * runtime_factor) - usage_penalty
    return round(min(max(score, 0), 100), 2)

# --- جلب أفضل البروكسيات حسب التقييم ---
def get_top_proxies(required_count=15, expected_duration=MAX_DURATION):
    all_proxies = list(proxy_db.items())
    scored = []

    for proxy, info in all_proxies:
        score = calculate_endurance_score(info, expected_duration)
        scored.append((proxy, score))

    top = [p for p in scored if p[1] >= 80]

    if len(top) < required_count:
        top += [p for p in scored if 70 <= p[1] < 80 and p not in top]

    if len(top) < required_count:
        for p in scored:
            if p not in top:
                top.append(p)
            if len(top) >= required_count:
                break

    top = sorted(top, key=lambda x: x[1], reverse=True)

    return [proxy for proxy, _ in top[:required_count]]

# --- نظام استبدال البروكسي ---
def replace_proxy(current_proxy, used_proxies=set(), required_count=20):
    candidates = get_top_proxies(required_count=required_count)
    candidates = [p for p in candidates if p not in used_proxies and p != current_proxy]

    if not candidates:
        return None

    return candidates[0]

# --- اختبار سريع لبروكسي ---
def quick_check(proxy, timeout=5):
    try:
        response = requests.get(BLOG_URL, proxies={
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }, timeout=timeout)
        return response.status_code == 200
    except:
        return False

# --- جلب العدد المطلوب من البروكسيات الأوروبية ---
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


# --- اختبار وتجهيز البروكسيات (تشغيل مباشر) ---
if __name__ == "__main__":
    print("📥 Fetching proxies from sources...")
    proxies = fetch_all_proxies()
    random.shuffle(proxies)

    print(f"🧪 Validating {len(proxies[:200])} proxies in parallel...")
    validate_proxies_parallel(proxies[:200])

    print("✅ Selecting top proxies by endurance score:")
    best = get_top_proxies()
    for p in best:
        print(f"✔️ {p}")
