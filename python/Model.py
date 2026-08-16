from datetime import date

import numpy as np


class PredictionModel:
    def loadData(self, data):
        self.model = {}
        self.itemCount = len(data)

        for entry in data:
            entry_date = date.fromisoformat(entry["date"])
            entry_name = entry["name"]

            entry_model = self.model.get(entry_name)
            if not entry_model:
                entry_model = {
                    "history": [],
                    "total": 0,
                    "dayOfWeek": np.zeros(7),
                    "dayOfMonth": np.zeros(31),
                    "dayOfYear": np.zeros(366),
                    "weekOfYear": np.zeros(53),
                    "monthOfYear": np.zeros(12),
                    "lastSale": np.zeros(62),
                }

            entry_model["dayOfWeek"][entry_date.weekday()] += 1
            entry_model["dayOfMonth"][entry_date.day - 1] += 1
            entry_model["dayOfYear"][
                (entry_date - date(entry_date.year, 1, 1)).days
            ] += 1
            entry_model["weekOfYear"][entry_date.isocalendar().week - 1] += 1
            entry_model["monthOfYear"][entry_date.month - 1] += 1

            history = entry_model["history"]
            if entry_model["total"] > 0:
                # We consider that there is at most 372 days between two sales
                # So we make 62 buckets of 6 days
                days = (entry_date - history[-1]).days
                bucket = min(days, 371) // 6
                entry_model["lastSale"][bucket] += 1

            # Update history
            history.append(entry_date)
            entry_model["total"] += 1

            self.model[entry_name] = entry_model

    def totalNormalize(self):
        for item in self.model:
            entry_model = self.model.get(item)
            entry_total = entry_model["total"]

            entry_model["dayOfWeek"] /= entry_total
            entry_model["dayOfMonth"] /= entry_total
            entry_model["dayOfYear"] /= entry_total
            entry_model["weekOfYear"] /= entry_total
            entry_model["monthOfYear"] /= entry_total
            entry_model["lastSale"] /= entry_total

    def minMaxNormalize(self):
        def op(array):
            minv = np.min(array)
            maxv = np.max(array)
            if maxv == minv:
                return np.full(array.shape, 0.6)  # TODO: test multiple values
            return ((array - minv) / (maxv - minv)) * 0.9 + 0.1

        for item in self.model:
            entry_model = self.model.get(item)

            entry_model["dayOfWeek"] = op(entry_model["dayOfWeek"])
            entry_model["dayOfMonth"] = op(entry_model["dayOfMonth"])
            entry_model["dayOfYear"] = op(entry_model["dayOfYear"])
            entry_model["weekOfYear"] = op(entry_model["weekOfYear"])
            entry_model["monthOfYear"] = op(entry_model["monthOfYear"])
            entry_model["lastSale"] = op(entry_model["lastSale"])

    def train(self, data):
        print("todo train")
