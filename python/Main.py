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
model.totalNormalize()
model.train(data["data"])
model.minMaxNormalize()

# ----------------------------------------------------------- Output

for item in model.model:
    for i, date in enumerate(model.model[item]["history"]):
        model.model[item]["history"][i] = date.strftime("%Y-%m-%d")

    model.model[item]["dayOfWeek"] = model.model[item]["dayOfWeek"].tolist()
    model.model[item]["dayOfMonth"] = model.model[item]["dayOfMonth"].tolist()
    model.model[item]["dayOfYear"] = model.model[item]["dayOfYear"].tolist()
    model.model[item]["weekOfYear"] = model.model[item]["weekOfYear"].tolist()
    model.model[item]["monthOfYear"] = model.model[item]["monthOfYear"].tolist()
    model.model[item]["lastSale"] = model.model[item]["lastSale"].tolist()

with open("model.json", "w", encoding="utf-8") as f:
    json.dump(model.model, f, ensure_ascii=False, indent=4)
