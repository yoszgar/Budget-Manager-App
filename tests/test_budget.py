import tempfile
from pathlib import Path


from budget_manager import services, storage


def assert_rejected(date, kind, category, amount, expected_word):
    """Helper: this input MUST raise ValueError mentioning expected_word."""
    try:
        services.add_transaction([], date, kind, category, amount)
    except ValueError as error:
        assert expected_word in str(error), str(error)
    else:
        assert False, f"{amount!r} should have been rejected"


def test_normal_add_and_summary():
    transactions = []
    services.add_transaction(transactions, "2026-09-01", "income", "salary", "2000")
    services.add_transaction(transactions, "2026-09-04", "expense", "food", "18.50")
    result = services.summarize(transactions)
    assert transactions[1]["id"] == "T002"
    assert result["income"] == 2000.0
    assert result["expense"] == 18.5
    assert result["balance"] == 1981.5


def test_boundary_bad_amounts():
    for bad in ["0", "-5", "abc", ""]:
        assert_rejected("2026-09-04", "expense", "food", bad, "amount")


def test_boundary_unknown_category_and_bad_date():
    assert_rejected("2026-09-04", "expense", "pets", "5", "category")
    assert_rejected("2026-02-30", "expense", "food", "5", "date")


def test_boundary_empty_summary():
    result = services.summarize([])
    assert result["balance"] == 0


def test_save_load_round_trip():
    transactions = []
    services.add_transaction(transactions, "2026-09-04", "expense", "food", "18.50")
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "t.json"
        storage.save_transactions(path, transactions)
        assert storage.load_transactions(path) == transactions


def test_backup_never_overwrites():
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "b.json"
        storage.backup_transactions([], path)
        try:
            storage.backup_transactions([], path)
        except ValueError:
            pass
        else:
            assert False, "second backup should have failed"


if __name__ == "__main__":
    for name, function in list(globals().items()):
        if name.startswith("test_"):
            function()
            print("PASS", name)