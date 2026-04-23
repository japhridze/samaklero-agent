import requests
import os


def send_dm(recipient_id: str, message: str) -> dict:
    """Instagram DM გაგზავნა Meta Graph API-ით"""
    url = "https://graph.facebook.com/v19.0/me/messages"
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message},
        "messaging_type": "RESPONSE",
        "access_token": os.getenv("INSTAGRAM_ACCESS_TOKEN")
    }
    resp = requests.post(url, json=payload, headers=headers)
    result = resp.json()

    if "error" in result:
        print(f"Instagram API შეცდომა: {result['error']}")
    
    return result
