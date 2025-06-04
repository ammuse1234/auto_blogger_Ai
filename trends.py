
import requests
from bs4 import BeautifulSoup

def get_trending_topics():
    url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # يرفع استثناء لو فيه خطأ مثل 404
        soup = BeautifulSoup(response.content, "xml")
        items = soup.find_all("item")
        topics = [item.title.text for item in items]
        return topics if topics else ["Latest news updates"]
    except Exception as e:
        print("Error fetching Google Trends:", e)
        return ["Latest news updates"]
