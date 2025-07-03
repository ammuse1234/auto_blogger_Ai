import random
import time
import threading
from proxy_manager import get_required_proxies, is_proxy_working, quick_check
from agent2 import Agent
import concurrent.futures 

def run_agent_with_auto_restart(agent_class, initial_proxy, remaining_proxies):
    proxy = initial_proxy

    while True:
        stop_event = threading.Event()

        def monitor_proxy():
            while not stop_event.is_set():
                time.sleep(0.25)
                if not quick_check(proxy):
                    print(f"🔌 Proxy failed during agent run: {proxy}")
                    stop_event.set()

        monitor_thread = threading.Thread(target=monitor_proxy, daemon=True)
        monitor_thread.start()

        agent = agent_class(proxy)

        try:
            agent.run()
            if not stop_event.is_set():
                return True  # ✅ Agent خلص بنجاح
            else:
                print("⚠️ Proxy failed mid-run. Restarting with new proxy...")
        except Exception as e:
            print(f"❌ Agent crashed: {e}")

        stop_event.set()
        time.sleep(15)

        if remaining_proxies:
            proxy = remaining_proxies.pop(0)
            print(f"🔁 Switching to new proxy: {proxy}")
        else:
            print("🔄 No remaining proxies. Fetching new proxy from proxy_manager...")
            new_proxies = get_required_proxies(required_count=1)
            if new_proxies:
                proxy = new_proxies[0]
                print(f"🆕 Using new proxy: {proxy}")
            else:
                print("❌ No new proxies found. Exiting.")
                return False
# ----------------- بداية البرنامج --------------------

# ✅ تحديد عدد الـ Agents عشوائيًا بين 5 و 10 (حسب طلبك سابقًا)
agent_count = random.randint(1,5)
print(f"🔢 Running {agent_count} agents...")

final_proxies = []
max_quick_attempts = 5
attempt = 0

# 🔄 محاولة جلب بروكسيات صالحة مع الفحص السريع وتعويض الفاشلة
while len(final_proxies) < agent_count and attempt < max_quick_attempts:
    needed = agent_count - len(final_proxies)
    print(f"\n🔄 Fetching {needed} proxies (Attempt {attempt + 1})...")

    new_proxies = get_required_proxies(required_count=needed)

    for proxy in new_proxies:
        print(f"⚡ Quick check for proxy: {proxy}")
        if is_proxy_working(proxy, timeout=5):
            final_proxies.append(proxy)
        else:
            print(f"❌ Proxy {proxy} failed quick check.")

    attempt += 1
    if len(final_proxies) < agent_count:
        print("♻️ Retrying to complete proxy list...")
        time.sleep(1)

# ⚠️ إذا ما قدرنا نحصل كل البروكسيات المطلوبة، نكمل باللي موجود
if len(final_proxies) < agent_count:
    print(f"⚠️ Only found {len(final_proxies)} working proxies out of {agent_count} requested.")
    agent_count = len(final_proxies)

# ✅ إنشاء وتشغيل كل Agent مع مراقبة البروكسي واستبداله عند الفشل
for i in range(agent_count):
    proxy = final_proxies[i]
    remaining = final_proxies[i+1:]  # البروكسيات المتبقية بعد هذا الـ Agent
    print(f"\n🚀 Starting Agent #{i+1} with proxy: {proxy}")

    try:
        run_agent_with_auto_restart(Agent, proxy, remaining)
    except Exception as e:
        print(f"❌ Error in Agent #{i+1}: {e}")

    sleep_time = random.randint(60, 180)
    print(f"⏳ Sleeping {sleep_time} seconds before next agent...")
    time.sleep(sleep_time)
    

with concurrent.futures.ThreadPoolExecutor(max_workers=agent_count) as executor:
    for i in range(agent_count):
        proxy = final_proxies[i]
        remaining = final_proxies[:i] + final_proxies[i+1:]
        executor.submit(run_agent_with_auto_restart, Agent, proxy, remaining)

print("✅ All agents completed.")
