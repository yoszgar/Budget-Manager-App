import math
from datetime import datetime

from budget_manager import models


def validate_transaction(date, kind, category, amount, currency):
    """Raise ValueError with a clear message if anything is wrong.
    Return the amount as a float if everything is fine."""
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except (TypeError, ValueError):
        raise ValueError(f"date must be a real date as YYYY-MM-DD, got {date!r}")

    if kind not in models.KINDS:
        raise ValueError(f"kind must be one of {models.KINDS}, got {kind!r}")

    if category not in models.CATEGORIES:
        raise ValueError(f"category must be one of {models.CATEGORIES}, got {category!r}")

    if currency not in models.CURRENCIES:
        raise ValueError(f"currency must be one of {models.CURRENCIES}, got {currency!r}")

    try:
        number = float(amount)
    except (TypeError, ValueError):
        raise ValueError(f"amount must be a number, got {amount!r}")
    if not math.isfinite(number) or number <= 0:
        raise ValueError(f"amount must be > 0, got {amount!r}")

    return number