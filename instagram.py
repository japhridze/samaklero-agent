import requests
import os

def send_dm(recipient_id: str, message: str) -> dict:
    token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    ig_user_id = os.getenv("INSTAGRAM_USER_ID", "17841433154370144")
    url = f"https://graph.facebook.com/v21.0/{ig_user_id}/messages"
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