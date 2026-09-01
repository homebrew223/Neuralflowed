import os, base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv
load_dotenv()

def send(html: str, to: str = None) -> bool:
    client_id = os.getenv("GMAIL_CLIENT_ID")
    client_secret = os.getenv("GMAIL_CLIENT_SECRET")
    refresh_token = os.getenv("GMAIL_REFRESH_TOKEN")
    if not all([client_id, client_secret, refresh_token]):
        print("Error: missing Gmail credentials in .env")
        raise SystemExit(1)
    creds = Credentials(
        None,
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
    )
    creds.refresh(Request())
    service = build("gmail", "v1", credentials=creds)
    msg = MIMEMultipart()
    msg["to"] = to or "me@example.com"
    msg["from"] = "me"
    msg["subject"] = "Newsletter"
    msg.attach(MIMEText(html, "html"))
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()
    return True
