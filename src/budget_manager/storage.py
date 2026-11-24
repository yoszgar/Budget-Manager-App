import csv
import json
from pathlib import Path


def load_transactions(path):
    path = Path(path)
    if not path.exists():
        return []  # first run: no file yet
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        raise ValueError(f"{path} is not valid JSON")
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON list")
    return data


def save_transactions(path, transactions):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Write to a temp file first, then swap it in, so a crash
    # in the middle of writing cannot destroy the real file.
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(json.dumps(transactions, indent=2))
    temp.replace(path)


def read_csv_rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def backup_transactions(transactions, destination):
    destination = Path(destination)
    if destination.exists():
        raise ValueError(f"backup file {destination} already exists, not overwriting")
    save_transactions(destination, transactions)