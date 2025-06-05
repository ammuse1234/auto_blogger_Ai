import os
import requests
from topics import get_trending_topic
from blogger import post_to_blogger

# إعداد Hugging Face API
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
    "Content-Type": "application/json"
}

# دالة توليد المقال
def generate_article(topic: str) -> str:
    prompt = f"Write a detailed and informative blog post about: {topic}"
    
    try:
        payload = {
            "inputs": prompt,
            "options": {
                "use_cache": False,
                "wait_for_model": True
            }
        }

        response = requests.post(API_URL, headers=headers, json=payload)
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
    post_to_blogger(topic, article)

if __name__ == "__main__":
    main()
