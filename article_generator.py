import os
import requests

# إعداد API Key من البيئة
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# ✅ نموذج مجاني مضمون يعمل على الخطة المجانية
MODEL_NAME = "HuggingFaceH4/zephyr-7b-beta"

def generate_article(topic: str) -> str:
    prompt = f"Write a detailed and informative blog post about: {topic}"

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 700,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL_NAME}",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        output = response.json()

        if isinstance(output, list) and "generated_text" in output[0]:
            return output[0]["generated_text"]
        else:
            return "⚠️ Failed to generate content. Response format unexpected."

    except Exception as e:
        print("❌ Error generating article with Hugging Face:", e)
        return "This is a default article content due to an error in generating the article."
