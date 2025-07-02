import random

# قائمة عناوين ونصوص جذابة متنوعة، يمكن تطويرها أو تعديلها حسب نوع المحتوى
MESSAGES_TEMPLATES = [
    "Check out this insightful read: {}",
    "Don't miss this article about: {}",
    "Here's something you’ll love: {}",
    "Discover the secrets behind: {}",
    "Top reasons why you should read: {}",
    "Get inspired by this post on: {}",
    "Must-read article: {}",
    "Everything you need to know about: {}",
    "Unlock new ideas with this: {}",
    "This article will change your perspective on: {}",
]

def generate_message(article_url):
    """
    توليد رسالة فريدة وجذابة بناءً على رابط المقالة.
    يمكنك تعديل هذه الدالة لتستخدم نصوص أو طرق أخرى حسب الحاجة.
    """
    # عادة نأخذ اسم المقالة من الرابط (يمكن تحسينها بجلب العنوان من المقال)
    # هنا ببساطة ناخذ آخر جزء من الرابط بدلًا من جلب العنوان الحقيقي
    article_title_part = article_url.rstrip('/').split('/')[-1].replace('-', ' ').title()
    
    template = random.choice(MESSAGES_TEMPLATES)
    message = template.format(article_title_part)
    return message
