import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_article(topic):
    prompt = f"Write a detailed blog post about: {topic}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=700
    )
    response.choices[0].message.content 
