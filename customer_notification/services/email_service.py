import boto3
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, SENDER_EMAIL
from services.template_service import render_template


def send_payment_reminder(email, name, amount, due_date):

    html_content = render_template(
        "payment_reminder.html",
        {
            "customer_name": name,
            "amount": amount,
            "due_date": due_date
        }
    )

    ses = boto3.client(
        "ses",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION,
    )

    ses.send_email(
        Source=SENDER_EMAIL,
        Destination={"ToAddresses": [email]},
        Message={
            "Subject": {"Data": "Payment Reminder - Invoice Overdue"},
            "Body": {
                "Html": {"Data": html_content}
            }
        }
    )