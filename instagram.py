import requests
import os

def send_dm(recipient_id: str, message: str) -> dict:
    """Instagram DM გაგზავნა Meta Graph API-ით"""
    
    INSTAGRAM_USER_ID = os.getenv("INSTAGRAM_USER_ID", "me")
    token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    
    url = f"https://graph.facebook.com/v21.0/{INSTAGRAM_USER_ID}/messages"
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message},
        "messaging_type": "RESPONSE",
        "access_token": token
    }
    
    resp = requests.post(url, json=payload, headers=headers)
    result = resp.json()
    
    if "error" in result:
        print(f"Instagram API შეცდომა: {result['error']}")
    
    return result