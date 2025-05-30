import requests
from bs4 import BeautifulSoup

def get_trending_topics():
    url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "xml")
    items = soup.find_all("item")
    topics = [item.title.text for item in items]
    return topics
