import boto3
from jinja2 import Environment, FileSystemLoader
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, SENDER_EMAIL


def send_payment_reminder(email, name, amount, due_date):

    # Load HTML template
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("payment_reminder.html")

    html_content = template.render(
        customer_name=name,
        amount=amount,
        due_date=due_date
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