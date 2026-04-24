import requests

token = "IGAAMZCWWZCehsFBZAFppVEtTZAVg5ZADhYU2pkVkRuWEJtVVE5TjB1TmswUEhadHJGNGRkQ500TEhDY19BZAXhMOGNPQ0N3STJYc3FJdG5qTjhYbWFwU2ZABXzBBN0llOG16RzUxT2hRN0hkV01fcWl6dHl4NGhjdDJpQzlzX3VSSGlodwZDZD"

r = requests.post(
    'https://graph.facebook.com/v19.0/17841433154370144/messages',
    json={
        'recipient': {'id': '1729219155105971'},
        'message': {'text': 'test'},
        'messaging_type': 'RESPONSE',
        'access_token': token
    }
)
print(r.json())