
def estimate_budget(days, budget_type):
    if budget_type == "Low":
        per_day = 2000
    elif budget_type == "Medium":
        per_day = 5000
    else:
        per_day = 10000

    total = per_day * days
    return f"Approximate trip cost: ₹{total}"
