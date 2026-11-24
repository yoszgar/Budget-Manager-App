# Allowed values (the "contract" every other module depends on).
KINDS = ["expense", "income"]
CATEGORIES = ["food", "transport", "rent", "salary", "entertainment", "health", "other"]
CURRENCIES = ["EUR"]  # Release 1 supports only EUR so totals are never mixed


def make_transaction(transaction_id, date, kind, category, amount, currency="EUR"):
    """Build one transaction. All 6 fields are always present."""
    return {
        "id": transaction_id,
        "date": date,
        "kind": kind,
        "category": category,
        "amount": amount,
        "currency": currency,
    }