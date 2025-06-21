import json
import os
import re

# 🔍 تحديد المسار الكامل لملف posted_articles.json داخل نفس مجلد السكربت

POSTED_FILE_PATH = os.path.join(os.getcwd(), "posted_articles.json")
# 🔄 دالة لتوحيد العنوان قبل حفظه أو مقارنته
def normalize_title(title: str) -> str:
    title = title.lower().strip()
    title = re.sub(r"[^\w\s]", "", title)  # إزالة الرموز مثل علامات التنصيص والنقاط
    title = re.sub(r"\s+", " ", title)     # إزالة الفراغات الزائدة
    return title

# 📥 تحميل العناوين المنشورة مسبقًا
def load_posted_titles():
    if os.path.exists(POSTED_FILE_PATH):
        with open(POSTED_FILE_PATH, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

# 💾 حفظ العنوان الجديد بعد تنسيقه
def save_posted_title(title):
    posted = load_posted_titles()
    normalized_title = normalize_title(title)
    if normalized_title not in posted:
        posted.append(normalized_title)
        
        # ✅ تأكد أن المجلد موجود (عادة ما يكون موجود مسبقًا)
        os.makedirs(os.path.dirname(POSTED_FILE_PATH), exist_ok=True)

        # 📝 حفظ الملف
        with open(POSTED_FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(posted, file, ensure_ascii=False, indent=2)
        
        print(f"✅ Saved title to {POSTED_FILE_PATH}")
    else:
        print(f"ℹ️ Title already exists: {normalized_title}")

# 🧠 فحص إذا تم نشر العنوان مسبقًا (بعد تنظيفه)
def is_duplicate(title):
    normalized_title = normalize_title(title)
    return normalized_title in load_posted_titles()
