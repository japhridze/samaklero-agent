from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os
from claude_agent import generate_reply
from instagram import send_dm

load_dotenv()
app = FastAPI()

# კონვერსაციის მეხსიერება (in-memory, მარტივი ვარიანტი)
# production-ისთვის გამოიყენე Redis ან SQLite
conversation_store: dict[str, list] = {}


@app.get("/webhook")
async def verify_webhook(request: Request):
    """Meta-ს webhook verification"""
    params = dict(request.query_params)
    verify_token = os.getenv("VERIFY_TOKEN")

    if (
        params.get("hub.mode") == "subscribe"
        and params.get("hub.verify_token") == verify_token
    ):
        print("Webhook verified!")
        return int(params.get("hub.challenge"))

    return {"error": "invalid verify token"}


@app.post("/webhook")
async def receive_message(request: Request):
    """Instagram DM-ების მიღება და პასუხი"""
    data = await request.json()
    print(f"Incoming: {data}")

    try:
        for entry in data.get("entry", []):
            for messaging in entry.get("messaging", []):
                sender_id = messaging["sender"]["id"]
                message_text = messaging.get("message", {}).get("text", "")

                # ხმოვანი/სტიკერი/ფოტო — გამოვტოვოთ
                if not message_text:
                    continue

                # კონვერსაციის ისტორია
                history = conversation_store.get(sender_id, [])

                # Claude-ის პასუხი
                reply = generate_reply(message_text, history)

                # ისტორიის განახლება (ბოლო 5 გაცვლა = 10 მესიჯი)
                history.append({"role": "user", "content": message_text})
                history.append({"role": "assistant", "content": reply})
                conversation_store[sender_id] = history[-10:]

                # Instagram-ში გაგზავნა
                send_dm(sender_id, reply)
                print(f"Replied to {sender_id}: {reply[:50]}...")

    except Exception as e:
        print(f"შეცდომა: {e}")

    # Meta-ს ყოველთვის უნდა დაუბრუნო 200
    return {"status": "ok"}


@app.get("/")
async def health():
    return {"status": "samaklero agent is running 🏠"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
