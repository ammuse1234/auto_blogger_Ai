import os
import google.generativeai as genai

# الحصول على المفتاح من المتغيرات البيئية
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# تفعيل المفتاح
genai.configure(api_key=GEMINI_API_KEY)

# إنشاء نموذج Gemini
model = genai.GenerativeModel("gemini-pro")

def generate_article(topic: str) -> str:
    prompt = f"Write a detailed, well-structured blog article about: {topic}. It should be informative, engaging, and formatted in markdown."

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("❌ Error generating article with Gemini:", e)
        return "This is a default article content due to an error in generating the article."
