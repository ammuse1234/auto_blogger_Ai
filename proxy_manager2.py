import requests
import random
import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# ✅ الدول الأوروبية المسموح بها
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

BLOG_URL = "https://ammuse12345.blogspot.com"
MAX_DURATION = 600  # أقصى مدة اختبار للبروكسي (10 دقائق)

# 🧠 قاعدة بيانات البروكسيات
proxy_db = {}

# ✅ تحديث إحصائيات البروكسي بعد كل اختبار
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

# ✅ اختبار بروكسي (فتح صفحة رئيسية ومقالة)
def is_proxy_working(proxy, timeout=8):
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    start_time = time.time()
    try:
        res = requests.get(BLOG_URL, proxies=proxies, timeout=timeout)
        if res.status_code != 200:
            raise Exception("Main page failed")
        soup = BeautifulSoup(res.text, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a') if a.get('href') and a.get('href').startswith(BLOG_URL) and a.get('href').endswith(".html")]
        if not links:
            raise Exception("No articles")
        art_res = requests.get(links[0], proxies=proxies, timeout=timeout)
        if art_res.status_code != 200:
            raise Exception("Article failed")
        duration = time.time() - start_time
        update_proxy_stats(proxy, True, duration)
        return True
    except:
        update_proxy_stats(proxy, False, 0)
        return False

# ✅ تحميل البروكسيات من مصدر واحد
def fetch_proxies_from_source(source_url):
    try:
        res = requests.get(source_url, timeout=10)
        proxies = res.text.strip().split("\n")
        return [p.strip() for p in proxies if ":" in p]
    except:
        return []

# ✅ تحميل البروكسيات من كل المصادر
def fetch_all_proxies():
    all_proxies = set()
    for url in PROXY_SOURCES:
        proxies = fetch_proxies_from_source(url)
        all_proxies.update(proxies)
    return list(all_proxies)

# ✅ فحص البروكسيات بالتوازي
def validate_proxies_parallel(proxy_list, max_workers=50):
    valid = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(is_proxy_working, proxy): proxy for proxy in proxy_list}
        for future in as_completed(futures):
            try:
                if future.result():
                    valid.append(futures[future])
            except:
                continue
    return valid

# ✅ تقييم تحمل البروكسي
def calculate_endurance_score(info, expected_duration=MAX_DURATION):
    success = info.get("success_count", 0)
    fail = info.get("fail_count", 0)
    used = info.get("currently_used_by", 0)
    avg_runtime = info.get("avg_runtime", expected_duration / 2)
    total = success + fail
    success_ratio = success / total if total > 0 else 0.5
    runtime_factor = min(avg_runtime / expected_duration, 2.0)
    usage_penalty = used * 5
    score = (success_ratio * 100 * runtime_factor) - usage_penalty
    return round(min(max(score, 0), 100), 2)

# ✅ الحصول على أعلى البروكسيات حسب التقييم
def get_top_proxies(required_count=15, expected_duration=MAX_DURATION):
    scored = []
    for proxy, info in proxy_db.items():
        score = calculate_endurance_score(info, expected_duration)
        scored.append((proxy, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    top = [p for p in scored if p[1] >= 80]
    if len(top) < required_count:
        top += [p for p in scored if 70 <= p[1] < 80 and p not in top]
    return [proxy for proxy, _ in top[:required_count]]

# ✅ استبدال بروكسي فاشل ببروكسي قوي
def replace_proxy(current_proxy, used_proxies=set(), required_count=20, allow_fetch=True):
    candidates = get_top_proxies(required_count=required_count)
    candidates = [p for p in candidates if p not in used_proxies and p != current_proxy]
    if candidates:
        return candidates[0]
    if allow_fetch:
        print("🔄 No valid proxy found. Fetching new proxies...")
        new_proxies = fetch_all_proxies()
        random.shuffle(new_proxies)
        validate_proxies_parallel(new_proxies[:200])
        return replace_proxy(current_proxy, used_proxies, required_count, allow_fetch=False)
    return None

# ✅ اختبار سريع لبروكسي فقط
def quick_check(proxy, timeout=5):
    try:
        res = requests.get(BLOG_URL, proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, timeout=timeout)
        return res.status_code == 200
    except:
        return False

# ✅ جلب عدد معين من البروكسيات الصالحة
def get_required_proxies(required_count=50, max_attempts=10):
    all_valid = set()
    for attempt in range(max_attempts):
        print(f"🔄 Attempt {attempt + 1}: Fetching proxies...")
        raw_proxies = fetch_all_proxies()
        random.shuffle(raw_proxies)
        valid = validate_proxies_parallel(raw_proxies)
        all_valid.update(valid)
        print(f"✅ Found {len(all_valid)} valid proxies so far.")
        if len(all_valid) >= required_count:
            break
        time.sleep(2)
    return list(all_valid)[:required_count]

# ✅ للتشغيل المباشر لاختبار النظام
if __name__ == "__main__":
    print("📥 Fetching proxies from sources...")
    proxies = fetch_all_proxies()
    random.shuffle(proxies)

    print(f"🧪 Validating first {len(proxies[:200])} proxies...")
    validate_proxies_parallel(proxies[:200])

    print("📊 Top proxies by endurance:")
    best get_top_proxies()
    for p in best:
        print(f"✔️ {p}")
