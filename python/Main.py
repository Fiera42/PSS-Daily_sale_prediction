import json

from FetchData import fetchData
from Model import PredictionModel

# ----------------------------------------------------------- Fetch

data = fetchData()
with open("raw_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# ----------------------------------------------------------- Load module

model = PredictionModel()
# model.loadData(data["data"][:-366])
model.loadData(data["data"])

# ----------------------------------------------------------- Output

for key in model.model:
    for i, date in enumerate(model.model[key]["history"]):
        model.model[key]["history"][i] = date.strftime("%Y-%m-%d")

with open("model.json", "w", encoding="utf-8") as f:
    json.dump(model.model, f, ensure_ascii=False, indent=4)
