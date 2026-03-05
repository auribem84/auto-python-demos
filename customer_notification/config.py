import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")

SENDER_EMAIL = os.getenv("SENDER_EMAIL")

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_ALERT_CHANNEL_ID = os.getenv("SLACK_ALERT_CHANNEL_ID")

CUSTOMER_DATA_FILE = "data/customers.csv"