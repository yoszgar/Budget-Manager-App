# Budget Manager (Release 1)

A command-line personal budget manager: add, list, summarize, import and back up transactions.

## Setup
Install [uv](https://docs.astral.sh/uv/), then:
```
uv sync
```

## Run
```
uv run python -m budget_manager.cli --help
uv run python -m budget_manager.cli import data/sample_transactions.csv
uv run python -m budget_manager.cli list
uv run python -m budget_manager.cli summary
uv run python -m budget_manager.cli add 2026-09-10 expense food 12.50
uv run python -m budget_manager.cli backup data/backup1.json
```

## Example
Importing the sample file imports 4 rows and rejects 3 with messages
such as `Row 5: amount must be > 0, got '-5'`.
`summary` then shows income 2000.00, expense 770.90, balance 1229.10.

## Test
```
uv run python -m pytest
```

## Known limitations
- EUR only
- Importing the same CSV twice creates duplicates
- No edit or delete command
- Money stored as floats (Release 2: use `decimal`)