from pytrends.request import TrendReq

def get_trending_topics():
    pytrends = TrendReq()
    pytrends.build_payload(kw_list=["news"])
    trending_searches = pytrends.trending_searches(pn="united_states")
    return trending_searches[0:5].tolist()