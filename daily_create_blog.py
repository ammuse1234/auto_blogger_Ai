from auth import get_authenticated_service
from blogger import create_blog
import datetime

def create_daily_blog():
    service = get_authenticated_service()
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    blog_title = f"AI Blog - {today}"
    blog_url = f"ai-blog-{today.replace('-', '')}"

    create_blog(service, blog_title, blog_url)

if __name__ == "__main__":
    create_daily_blog()
