import csv
from io import StringIO
from .schema import Expense

def parse_csv(csv_text: str) -> list[Expense]:
    reader = csv.DictReader(StringIO(csv_text))
    return [
        Expense(
            category=row["category"],
            subcategory=row["subcategory"],
            amount=float(row["amount"]),
            frequency=row["frequency"],
            essential=row["essential"].lower() == "true"
        )
        for row in reader
    ]
