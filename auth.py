import os
import json
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# تحميل بيانات الاعتماد من ملف JSON
def get_authenticated_service():
    creds_path = os.getenv("GOOGLE_CREDENTIALS_FILE", "client_secret.json")
    if not os.path.exists(creds_path):
        raise FileNotFoundError(f"Credentials file not found: {creds_path}")

    with open(creds_path, "r") as f:
        creds_data = json.load(f)

    creds = Credentials.from_authorized_user_info(info=creds_data)

    # التأكد من صلاحية التوكن
    if creds.expired and creds.refresh_token:
        creds.refresh(google.auth.transport.requests.Request())

    # خدمة blogger
    service = build("blogger", "v3", credentials=creds)
    return service
