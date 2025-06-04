import os
import google.generativeai as genai

# إعداد API key
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def generate_article(topic: str) -> str:
    prompt = f"Write a detailed and informative blog post about: {topic}"
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("❌ Error generating article with Gemini:", e)
        return "This is a default article content due to an error in generating the article."
