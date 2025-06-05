import os
import requests
from topic_generator import get_trending_topic
from blogger import post_to_blogger

# إعداد متغيرات البيئة
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BLOG_ID = os.getenv("BLOG_ID") 
# دالة توليد Access Token من Google
def get_access_token():
    print("🔐 Getting access token from Google...")
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }

    try:
        res = requests.post(token_url, data=payload)
        res.raise_for_status()
        access_token = res.json().get("access_token")
        return access_token
    except Exception as e:
        print("❌ Error getting access token:", e)
        return None

# دالة توليد المقال من Hugging Face
def generate_article(topic: str) -> str:
    prompt = f"Write a detailed and informative blog post about: {topic}"
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "options": {
            "use_cache": False,
            "wait_for_model": True
        }
    }

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"].strip()
        else:
            print("⚠️ Unexpected Hugging Face response:", result)
            return "This is a default article content due to an error in generating the article."
    except Exception as e:
        print("❌ Error generating article with Hugging Face:", e)
        return "This is a default article content due to an error in generating the article."

# الدالة الرئيسية
def main():
    topic = get_trending_topic()
    print(f"✍️ توليد مقال عن: {topic}")
    article = generate_article(topic)
    access_token = get_access_token()
    if access_token:
        post_to_blogger(BLOG_ID, topic, article, access_token)
    else:
        print("❌ Failed to get access token. Skipping post.")

if __name__ == "__main__":
    main()
