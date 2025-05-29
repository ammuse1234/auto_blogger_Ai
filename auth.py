import os
import json
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def get_access_token():
    creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/blogger"])
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return creds.token