def predict(model, date):
    res_add = {}
    res_mult = {}
    res_add_sum = 0
    res_mult_sum = 0

    for item in model.model:
        entry_model = model.model.get(item)
        history = entry_model["history"]

        dayOfWeek = entry_model["dayOfWeek"][date.weekday()]
        dayOfMonth = entry_model["dayOfMonth"][date.day - 1]
        dayOfYear = entry_model["dayOfYear"][(date - date(date.year, 1, 1)).days]
        weekOfYear = entry_model["weekOfYear"][date.isocalendar().week - 1]
        monthOfYear = entry_model["monthOfYear"][date.month - 1]
        lastSale = entry_model["lastSale"][min((date - history[-1]).days, 371) // 6]

        res_add[item] = (
            (dayOfWeek + dayOfMonth + dayOfYear + weekOfYear + monthOfYear + lastSale)
            / 6  # Normalize to 1
            * (entry_model["total"] / model.itemCount)  # Baseline probability
        )
        res_add_sum += res_add[item]
        res_mult[item] = (
            (dayOfWeek * dayOfMonth * dayOfYear * weekOfYear * monthOfYear * lastSale)
            * (entry_model["total"] / model.itemCount)  # Baseline probability
        )
        res_mult_sum += res_mult[item]

    # Link items
    for item in model.model:
        res_add[item] /= res_add_sum
        res_mult[item] /= res_mult_sum

    return (res_add, res_mult)


def evaluate_all(data, model):
    print("todo: evaluate all")
    # Return a value between 0 and 100 for the accuracy of the model on ALL data


def evaluate_one(model, date, answer):
    p = predict(model, date)
    return p[answer]
