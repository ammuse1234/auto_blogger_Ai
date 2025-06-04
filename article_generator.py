import os
import google.generativeai as genai

# إعداد API key
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def generate_article(topic: str) -> str:
    prompt = f"Write a detailed and informative blog post in English about: {topic}"
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        # تحقق من وجود نص فعلي
        if hasattr(response, 'text') and response.text.strip():
            return response.text.strip()
        else:
            print("⚠️ Gemini API returned an empty response.")
            return "This is a default article content due to empty response from Gemini."

    except Exception as e:
        print("❌ Error generating article with Gemini:")
        print(e)  # طباعة الخطأ بالكامل
        return "This is a default article content due to an error in generating the article."
