import os
from openai import OpenAI
import openai

client = OpenAI()

def generate_article(topic):
    prompt = f"Write a detailed blog post about: {topic}"
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # استخدم موديل متاح للجميع
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=700
        )
        return response.choices[0].message.content
    except openai.error.OpenAIError as e:
        print(f"❌ Error generating article: {e}")
        return "Sorry, there was an error generating the article."
