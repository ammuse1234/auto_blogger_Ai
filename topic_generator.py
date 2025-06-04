from pytrends.request import TrendReq
import random

def get_trending_topic():
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        trending_searches_df = pytrends.trending_searches(pn='united_states')

        if not trending_searches_df.empty:
            topics = trending_searches_df[0].tolist()
            return random.choice(topics)
        else:
            return "Latest technology trends"
    except Exception as e:
        print("Error fetching Google Trends:", e)
        return "Latest news updates"
