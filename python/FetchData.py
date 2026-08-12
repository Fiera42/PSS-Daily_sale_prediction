import json

import requests

url = "https://pixyship.com/api/lastsalesbysalefrom/shop"

headers = {
    "Accept": "application/json, text/plain, */*",
    "host": "pixyship.com",
    "Referer": "https://pixyship.com/dailysales/shop",
}

response = requests.get(url, headers=headers).json()

print(response["current_time"])
#print(response["data"])

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(response, f, ensure_ascii=False, indent=4)
