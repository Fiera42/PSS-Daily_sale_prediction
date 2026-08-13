import json
from datetime import date, timedelta

import requests

# ----------------------------------------------------------- Fetch data

url = "https://pixyship.com/api/lastsalesbysalefrom/shop"

headers = {
    "Accept": "application/json, text/plain, */*",
    "host": "pixyship.com",
    "Referer": "https://pixyship.com/dailysales/shop",
}

json_data = requests.get(url, headers=headers).json()


# ----------------------------------------------------------- Clean data

KEEP_KEYS = {"date", "id", "name", "price", "type"}
delta = timedelta(days=1)

seen = set()
cleaned_data = []

for entry in reversed(json_data["data"]):
    entry_date = date.fromisoformat(entry["date"][:10])
    entry_id = entry["id"]

    if (entry_date - delta, entry_id) in seen:
        continue

    seen.add((entry_date, entry_id))

    cleaned_data.append(
        {key: value for key, value in entry.items() if key in KEEP_KEYS}
    )

json_data["data"] = cleaned_data
count = len(cleaned_data)

# ----------------------------------------------------------- Output

print(json_data["current_time"])
# print(response["data"])

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)
