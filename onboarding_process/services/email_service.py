import boto3
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, SENDER_EMAIL

def send_welcome_email(to_email, customer_name):
    ses = boto3.client(
        "ses",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION,
    )

    subject = "Welcome to Our Platform 🎉"

    body_text = f"""
Hi {customer_name},

Welcome aboard!

Your environment has been successfully created.
Our team will contact you shortly.

Best regards,
The Team
"""

    ses.send_email(
        Source=SENDER_EMAIL,
        Destination={"ToAddresses": [to_email]},
        Message={
            "Subject": {"Data": subject},
            "Body": {"Text": {"Data": body_text}},
        },
    )