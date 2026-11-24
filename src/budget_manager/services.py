from budget_manager import models, validation


def next_id(transactions):
    return "T" + str(len(transactions) + 1).zfill(3)  # T001, T002, ...


def add_transaction(transactions, date, kind, category, amount, currency="EUR"):
    clean_amount = validation.validate_transaction(date, kind, category, amount, currency)
    transaction = models.make_transaction(
        next_id(transactions), date, kind, category, clean_amount, currency
    )
    transactions.append(transaction)
    return transaction


def filter_transactions(transactions, kind=None, category=None):
    result = []
    for t in transactions:
        if kind is not None and t["kind"] != kind:
            continue
        if category is not None and t["category"] != category:
            continue
        result.append(t)
    return result


def summarize(transactions):
    income = 0.0
    expense = 0.0
    expense_by_category = {}
    for t in transactions:
        if t["kind"] == "income":
            income += t["amount"]
        else:
            expense += t["amount"]
            old_total = expense_by_category.get(t["category"], 0)
            expense_by_category[t["category"]] = old_total + t["amount"]
    return {
        "income": income,
        "expense": expense,
        "balance": income - expense,
        "expense_by_category": expense_by_category,
    }