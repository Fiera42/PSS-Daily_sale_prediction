from datetime import date, timedelta

import requests


def fetchData():
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
        entry_name = entry["name"]

        if (entry_date - delta, entry_name) in seen:
            continue

        seen.add((entry_date, entry_name))

        cleaned_data.append(
            {key: value for key, value in entry.items() if key in KEEP_KEYS}
        )
        cleaned_data[-1]["date"] = entry["date"][:10]

    json_data["data"] = cleaned_data
    # count = len(cleaned_data)

    # ----------------------------------------------------------- Output

    if not json_data["current_time"]:
        raise RuntimeError("Fetch failed")

    print(json_data["current_time"])
    return json_data
