import boto3
from botocore.exceptions import ClientError
from app.config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, SENDER_EMAIL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

def send_invoice(to_email, pdf_path, invoice_number):

    ses = boto3.client(
        "ses",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION,
    )

    # Crear mensaje
    msg = MIMEMultipart()
    msg["Subject"] = f"Invoice #{invoice_number}"
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    # Cuerpo del email
    body = MIMEText("Please find attached your invoice.", "plain")
    msg.attach(body)

    # Adjuntar PDF
    with open(pdf_path, "rb") as f:
        part = MIMEApplication(f.read(), Name=os.path.basename(pdf_path))
        part["Content-Disposition"] = f'attachment; filename="{os.path.basename(pdf_path)}"'
        msg.attach(part)

    try:
        ses.send_raw_email(
            Source=SENDER_EMAIL,
            Destinations=[to_email],
            RawMessage={"Data": msg.as_string()},
        )
        print("Email sent successfully.")
    except ClientError as e:
        print("Error sending email:", e)