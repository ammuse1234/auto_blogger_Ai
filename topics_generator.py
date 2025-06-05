from pytrends.request import TrendReq
import random
from utils import is_duplicate

fallback_topics = [
    "Artificial Intelligence 2025",
    "Climate Change Effects",
    "SpaceX Mars Mission",
    "Cryptocurrency Regulations",
    "iPhone 17 Rumors",
    "New Electric Cars 2025",
    "Best AI Tools This Year",
    "Future of Work in AI Era",
    "Mental Health Awareness Trends",
    "Clean Energy Innovations"
]

def get_trending_topic():
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        trending_searches_df = pytrends.trending_searches(pn='united_states')

        if not trending_searches_df.empty:
            topics = trending_searches_df[0].tolist()
            random.shuffle(topics)
            for topic in topics:
                if not is_duplicate(topic):
                    return topic
            print("⚠️ All trending topics were already used. Using fallback.")
    except Exception as e:
        print("❌ Error fetching Google Trends:", e)

    # إذا فشل كل شيء، اختر من القائمة الاحتياطية وتجنب التكرار
    fallback_available = [t for t in fallback_topics if not is_duplicate(t)]
    if fallback_available:
        return random.choice(fallback_available)
    else:
        return random.choice(fallback_topics)  # fallback نهائي حتى لو مكرر
