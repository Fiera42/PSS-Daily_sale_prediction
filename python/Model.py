from datetime import date


class PredictionModel:
    def loadData(self, data):
        self.model = {}
        for entry in data:
            entry_date = date.fromisoformat(entry["date"])
            entry_name = entry["name"]

            entry_model = self.model.get(entry_name)
            if not entry_model:
                entry_model = {
                    "history": [],
                    "dayOfWeek": [0] * 7,
                    "dayOfMonth": [0] * 31,
                    "dayOfYear": [0] * 366,
                    "weekOfYear": [0] * 53,
                    "monthOfYear": [0] * 12,
                    "lastSale": [0] * 62,
                }
            history = entry_model["history"]

            entry_model["dayOfWeek"][entry_date.weekday()] += 1
            entry_model["dayOfMonth"][entry_date.day - 1] += 1
            entry_model["dayOfYear"][
                (entry_date - date(entry_date.year, 1, 1)).days
            ] += 1
            entry_model["weekOfYear"][entry_date.isocalendar().week - 1] += 1
            entry_model["monthOfYear"][entry_date.month - 1] += 1
            if len(history) > 0:
                # We consider that there is at most 372 days between two sales
                # So we make 62 buckets of 6 days
                days = (entry_date - history[-1]).days
                bucket = min(days, 371) // 6
                entry_model["lastSale"][bucket] += 1

            # Keep most recent data
            history.append(entry_date)

            self.model[entry_name] = entry_model
