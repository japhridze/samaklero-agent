import requests
import os

def send_dm(recipient_id: str, message: str) -> dict:
<<<<<<< HEAD
    token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    ig_user_id = os.getenv("INSTAGRAM_USER_ID", "17841433154370144")
    url = f"https://graph.facebook.com/v21.0/{ig_user_id}/messages"
=======
    """Instagram DM გაგზავნა Meta Graph API-ით"""
    
    INSTAGRAM_USER_ID = os.getenv("INSTAGRAM_USER_ID", "me")
    token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    
    url = f"https://graph.facebook.com/v21.0/{INSTAGRAM_USER_ID}/messages"
    
>>>>>>> 95dc5c3feaa4e4da6b1d5446850171895f521045
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message},
        "messaging_type": "RESPONSE",
        "access_token": token
    }
    resp = requests.post(url, json=payload, headers=headers)
    result = resp.json()
    print(f"Instagram API პასუხი: {result}")
    return result