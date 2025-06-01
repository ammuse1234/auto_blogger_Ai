import os
from blogger import create_blog
import requests

def get_access_token():
    """استخراج access token باستخدام refresh token الموجود في GitHub Secrets"""
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']
    refresh_token = os.environ['REFRESH_TOKEN']

    token_url = 'https://oauth2.googleapis.com/token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }

    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"❌ Failed to get access token: {response.text}")

def main():
    # إعدادات المدونة الجديدة
    blog_title = "Daily AI Blog"
    blog_description = "This blog is automatically created using AI and Blogger API."

    # استخراج التوكن
    access_token = get_access_token()

    # إنشاء المدونة
    create_blog(blog_title, blog_description, access_token)

if __name__ == "__main__":
    main() 
