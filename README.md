# სამაკლერო Instagram Agent 🏠

AI agent რომელიც კითხულობს ობიექტებს Google Sheets-დან და პასუხობს Instagram DM-ებზე.

---

## დაყენება — ნაბიჯ-ნაბიჯ

### ნაბიჯი 1 — Python პაკეტები

```bash
pip install -r requirements.txt
```

---

### ნაბიჯი 2 — Google Sheets წვდომა

1. გადადი: https://console.cloud.google.com
2. შექმენი ახალი Project
3. ჩართე **Google Sheets API** (APIs & Services → Enable APIs)
4. შექმენი **Service Account** (APIs & Services → Credentials → Create Credentials)
5. Service Account-ზე გენერირე JSON key → გადმოწერე
6. გადარქვი სახელი: `credentials.json` და ჩააგდე პროექტის საქაღალდეში
7. **მნიშვნელოვანი:** გახსენი credentials.json, იპოვე `client_email` და **გააზიარე Sheet ამ email-ზე** (Viewer წვდომა)

---

### ნაბიჯი 3 — .env ფაილი

```bash
cp .env.example .env
```

შეავსე `.env`:
- `ANTHROPIC_API_KEY` → https://console.anthropic.com
- `SHEET_ID` → Google Sheet URL-დან (`.../spreadsheets/d/XXXXX/edit`)
- `VERIFY_TOKEN` → თავად მოიფიქრე (მაგ: `samaklero2024`)
- `INSTAGRAM_ACCESS_TOKEN` → Meta Developer-დან (ნაბიჯი 4)

---

### ნაბიჯი 4 — Meta / Instagram App

1. გადადი: https://developers.facebook.com
2. შექმენი App → Business type
3. დაამატე **Instagram** product
4. Basic Display API → Instagram User Access Token (გამოცდისთვის)
5. Production-ისთვის: Messenger API for Instagram

---

### ნაბიჯი 5 — სერვერზე გაშვება (Railway)

1. გადადი: https://railway.app
2. New Project → Deploy from GitHub
3. Environment Variables-ში დაამატე `.env`-ის მნიშვნელობები
4. მიიღე public URL (მაგ: `https://samaklero.railway.app`)

---

### ნაბიჯი 6 — Webhook დაყენება

Meta Developer Console-ში:
- Webhook URL: `https://შენი-სერვერი.railway.app/webhook`
- Verify Token: ის რაც `.env`-ში დაწერე
- Subscribe to: `messages`

---

### ლოკალური ტესტი

```bash
# სერვერის გაშვება
python main.py

# სხვა ტერმინალში — webhook სიმულაცია
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "entry": [{
      "messaging": [{
        "sender": {"id": "test123"},
        "message": {"text": "გაქვთ 2 ოთახიანი ბინა ვაკეში?"}
      }]
    }]
  }'
```

---

## ფაილების სტრუქტურა

```
samaklero-agent/
├── main.py           # FastAPI სერვერი + webhook
├── sheets.py         # Google Sheets კავშირი
├── claude_agent.py   # AI პასუხის გენერაცია
├── instagram.py      # DM გაგზავნა
├── credentials.json  # Google Service Account (არ ატვირთო GitHub-ზე!)
├── .env              # API გასაღებები (არ ატვირთო GitHub-ზე!)
├── .env.example      # შაბლონი
└── requirements.txt
```

---

## Google Sheet სტრუქტურა

### ჩანართი: `ობიექტები`
| ID | სახელი | ტიპი | ოთახები | ფასი | ადგილმდებარეობა | ფართი_მ2 | სართული | სტატუსი | აღწერა | ფოტო_ლინკი |

### ჩანართი: `FAQ`
| კითხვა | პასუხი |

---

## მნიშვნელოვანი

`.gitignore` ფაილში დაამატე:
```
credentials.json
.env
```
