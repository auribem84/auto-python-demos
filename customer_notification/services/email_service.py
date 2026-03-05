import boto3
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, SENDER_EMAIL


def send_payment_reminder(email, name, amount, due_date):
    ses = boto3.client(
        "ses",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION,
    )

    subject = "Payment Reminder - Invoice Overdue"

    body = f"""
Hello {name},

This is a reminder that your payment of ${amount}
due on {due_date} is overdue.

Please process the payment at your earliest convenience.

Thank you.
"""

    ses.send_email(
        Source=SENDER_EMAIL,
        Destination={"ToAddresses": [email]},
        Message={
            "Subject": {"Data": subject},
            "Body": {"Text": {"Data": body}},
        },
    )