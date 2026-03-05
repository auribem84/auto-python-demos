from services.data_service import get_overdue_customers
from services.email_service import send_payment_reminder
from services.slack_service import notify_internal_team


def process_notifications():
    customers = get_overdue_customers()

    for customer in customers:
        name = customer["customer_name"]
        email = customer["email"]
        amount = customer["amount_due"]
        due_date = customer["due_date"]

        send_payment_reminder(email, name, amount, due_date)
        notify_internal_team(name, amount)

        print(f"Reminder sent to {name}")