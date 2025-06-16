import os
import re
import urllib.parse
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

# دالة توليد مقال باستخدام Gemini
def generate_article(topic: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key=AIzaSyDSOgakd0CgLzG0h8C1ZXIjMV7OavNax9c"
    
    headers = {
        "Content-Type": "application/json"
    }

    prompt = f"""Write a detailed and informative blog post about: {topic}.It should be informative, engaging, and formatted well.
 Use:
- A friendly introduction  
- Clear subheadings  
- Natural tone and smooth flow  
- Short paragraphs  
- A personal or reflective conclusion  
Avoid robotic language, repetition, or markdown. Output plain text only. Around 800 words."""
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        print("❌ Error generating article with Gemini:", e)
        return "This is a default article content due to an error in generating the article."
        
def get_image_html(topic: str) -> str:
    base_url = "https://source.unsplash.com/800x400/?"
    query = urllib.parse.quote(topic)
    image_url = f"{base_url}{query}"
    
    # التحقق من صلاحية الرابط
    try:
        test_response = requests.get(image_url, timeout=5)
        if test_response.status_code != 200 or "image" not in test_response.headers.get("Content-Type", ""):
            # إذا الرابط ما جاب صورة، استخدم كلمة بديلة
            image_url = f"{base_url}technology"
    except:
        image_url = f"{base_url}technology"

    return f'<img src="{image_url}" alt="{topic}" style="max-width:100%;height:auto;border-radius:12px;margin-bottom:15px;">'

def format_article(article: str, title: str) -> str:
    # 🔧 تنظيف التنسيقات
    article = re.sub(r"\*{1,2}(.*?)\*{1,2}", r"\1", article)
    article = re.sub(r"\_{1,2}(.*?)\_{1,2}", r"\1", article)
    article = re.sub(r"^\s*>\s*", "", article, flags=re.MULTILINE)
    article = re.sub(r".*?.*?", "", article)
    article = re.sub(r"\!.*?.*?", "", article)
    article = re.sub(r".*?", "", article)
    article = re.sub(r"---+", "", article)
    article = re.sub(r"\*\s+", "", article)

    # ✨ تنسيق الفقرات
    paragraphs = article.split("\n")
    formatted_paragraphs = [f"<p>{p.strip()}</p>" for p in paragraphs if p.strip()]

    # 🖼️ إضافة صورة أول المقال
    image_html = get_image_html(title)

    # 🏷️ بناء المقال النهائي
    formatted_article = f"<h2>{title}</h2>\n{image_html}\n" + "\n".join(formatted_paragraphs) + "\n<hr>"
    return formatted_article

# الدلة الرئيسية
def main():
    topic = get_trending_topic()
    print(f"✍️ توليد مقال عن: {topic}")
    article = generate_article(topic)
    formatted_article = format_article(article, topic)
    access_token = get_access_token()
    if access_token:
        post_to_blogger(BLOG_ID, topic, formatted_article, access_token)
    else:
        print("❌ Failed to get access token. Skipping post.")

if __name__ == "__main__":
    main()
