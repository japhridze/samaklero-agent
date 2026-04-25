from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os
import httpx
from claude_agent import generate_reply

load_dotenv()
app = FastAPI()

conversation_store: dict[str, list] = {}

PAGE_TOKEN = os.getenv("FACEBOOK_PAGE_TOKEN")
INSTAGRAM_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

@app.get("/webhook")
async def verify_webhook(request: Request):
    params = dict(request.query_params)
    if (
        params.get("hub.mode") == "subscribe"
        and params.get("hub.verify_token") == VERIFY_TOKEN
    ):
        print("Webhook verified!")
        return int(params.get("hub.challenge"))
    return {"error": "invalid verify token"}

async def send_facebook_message(sender_id: str, text: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://graph.facebook.com/v19.0/me/messages",
            params={"access_token": PAGE_TOKEN},
            json={
                "recipient": {"id": sender_id},
                "message": {"text": text}
            }
        )
        print(f"FB response: {response.status_code} {response.text}")

async def send_instagram_message(sender_id: str, text: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://graph.facebook.com/v19.0/me/messages",
            params={"access_token": INSTAGRAM_TOKEN},
            json={
                "recipient": {"id": sender_id},
                "message": {"text": text}
            }
        )
        print(f"IG response: {response.status_code} {response.text}")

@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    print(f"Incoming: {data}")

    try:
        for entry in data.get("entry", []):
            # გავარჩიოთ Instagram და Facebook
            is_instagram = "instagram" in str(entry.get("id", "")) or entry.get("object") == "instagram"
            
            for messaging in entry.get("messaging", []):
                sender_id = messaging["sender"]["id"]
                message_text = messaging.get("message", {}).get("text", "")

                if not message_text:
                    continue

                history = conversation_store.get(sender_id, [])
                reply = generate_reply(message_text, history)

                history.append({"role": "user", "content": message_text})
                history.append({"role": "assistant", "content": reply})
                conversation_store[sender_id] = history[-10:]

                if is_instagram:
                    await send_instagram_message(sender_id, reply)
                else:
                    await send_facebook_message(sender_id, reply)

                print(f"Replied to {sender_id}: {reply[:50]}...")

    except Exception as e:
        print(f"შეცდომა: {e}")

    return {"status": "ok"}

@app.get("/")
async def health():
    return {"status": "samaklero agent is running 🏠"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)