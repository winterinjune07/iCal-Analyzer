import csv
import os
import sys
from collections import defaultdict
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

from dotenv import load_dotenv

DATE_FORMAT = "%m-%d-%Y"
COLUMNS = {
    "check": "Check Date",
    "start": "Pay Period Start",
    "end": "Pay Period End",
}
CENT = Decimal("0.01")

### INPUT CSV
input_csv = "./data/output-data.csv"

def money(value: Decimal) -> str:
    return str(value.quantize(CENT, rounding=ROUND_HALF_UP))


def monthly_totals(path: str, by: str) -> dict:
    date_col = COLUMNS[by]
    totals = defaultdict(lambda: {"hours": Decimal(0), "gross": Decimal(0), "net": Decimal(0)})

    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if not any((v or "").strip() for v in row.values()):
                continue  # skip blank lines
            month = datetime.strptime(row[date_col].strip(), DATE_FORMAT).strftime("%Y-%m")
            totals[month]["hours"] += Decimal(row["Hours"])
            totals[month]["gross"] += Decimal(row["Gross Pay"])
            totals[month]["net"] += Decimal(row["Net Pay"])

    return dict(sorted(totals.items()))


def main() -> None:
    load_dotenv(Path(__file__).resolve().with_name(".env"))
    by = (os.getenv("GROUP_BY") or "check").strip().lower()
    out = ("./data/monthly-totals.csv").strip()

    if not input_csv:
        sys.exit("INPUT_CSV is not set in .env")
    if not Path(input_csv).is_file():
        sys.exit(f"INPUT_CSV not found: {input_csv}")
    if by not in COLUMNS:
        sys.exit(f"Invalid GROUP_BY '{by}' in .env. Use one of: {', '.join(COLUMNS)}")

    totals = monthly_totals(input_csv, by)
    header = ["Month", "Hours", "Gross Pay", "Net Pay"]
    rows = [[m, str(t["hours"]), money(t["gross"]), money(t["net"])] for m, t in totals.items()]

    if out:
        with open(out, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)
    else:
        writer = csv.writer(sys.stdout, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


if __name__ == "__main__":
    main()