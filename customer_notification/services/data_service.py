import csv
from datetime import datetime
from config import CUSTOMER_DATA_FILE


def get_overdue_customers():
    overdue = []

    today = datetime.today().date()

    with open(CUSTOMER_DATA_FILE, newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            due_date = datetime.strptime(row["due_date"], "%Y-%m-%d").date()

            if due_date < today:
                overdue.append({
                    "customer_name": row["customer_name"],
                    "email": row["email"],
                    "amount_due": row["amount_due"],
                    "due_date": row["due_date"]
                })

    return overdue