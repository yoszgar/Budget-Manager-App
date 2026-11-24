import argparse
import sys
from pathlib import Path

from budget_manager import services, storage

# Always <project>/data/transactions.json, whatever folder you run from.
DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "transactions.json"


def build_parser():
    parser = argparse.ArgumentParser(description="Personal budget manager")
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="add one transaction")
    add.add_argument("date", help="YYYY-MM-DD")
    add.add_argument("kind", help="expense or income")
    add.add_argument("category")
    add.add_argument("amount")
    add.add_argument("--currency", default="EUR")

    show = commands.add_parser("list", help="show transactions")
    show.add_argument("--kind")
    show.add_argument("--category")

    commands.add_parser("summary", help="show totals")

    backup = commands.add_parser("backup", help="save a copy of the data")
    backup.add_argument("destination")

    load = commands.add_parser("import", help="import transactions from a CSV file")
    load.add_argument("csv_file")

    return parser


def format_transaction(t):
    return (f"{t['id']}  {t['date']}  {t['kind']:<8} "
            f"{t['category']:<14} {t['amount']:>10.2f} {t['currency']}")


def run_add(args, transactions):
    t = services.add_transaction(
        transactions, args.date, args.kind, args.category, args.amount, args.currency
    )
    storage.save_transactions(DATA_FILE, transactions)
    print("Added " + format_transaction(t))
    return 0


def run_list(args, transactions):
    for t in services.filter_transactions(transactions, args.kind, args.category):
        print(format_transaction(t))
    return 0


def run_summary(args, transactions):
    s = services.summarize(transactions)
    print(f"Transactions: {len(transactions)}")
    print(f"Income:  {s['income']:.2f} EUR")
    print(f"Expense: {s['expense']:.2f} EUR")
    print(f"Balance: {s['balance']:.2f} EUR")
    for category, total in s["expense_by_category"].items():
        print(f"  {category}: {total:.2f}")
    return 0


def run_backup(args, transactions):
    storage.backup_transactions(transactions, args.destination)
    print("Backup saved to " + args.destination)
    return 0


def run_import(args, transactions):
    rows = storage.read_csv_rows(args.csv_file)
    added = 0
    rejected = 0
    for number, row in enumerate(rows, start=2):  # row 1 is the header
        try:
            services.add_transaction(
                transactions,
                row.get("date"), row.get("kind"), row.get("category"),
                row.get("amount"), row.get("currency", "EUR"),
            )
            added += 1
        except ValueError as error:
            print(f"Row {number}: {error}", file=sys.stderr)
            rejected += 1
    storage.save_transactions(DATA_FILE, transactions)
    print(f"Imported {added} rows, rejected {rejected} rows")
    return 1 if rejected else 0


COMMANDS = {
    "add": run_add,
    "list": run_list,
    "summary": run_summary,
    "backup": run_backup,
    "import": run_import,
}


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        transactions = storage.load_transactions(DATA_FILE)
        return COMMANDS[args.command](args, transactions)
    except (ValueError, OSError) as error:
        print("error: " + str(error), file=sys.stderr)  # errors go to stderr
        return 1


if __name__ == "__main__":
    sys.exit(main())  # exit code 0 = success, 1 = error