import os
from dotenv import load_dotenv

load_dotenv()

# ==============================
# AWS
# ==============================
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")

# ==============================
# PostgreSQL
# ==============================
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# ==============================
# Slack
# ==============================
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_ONBOARDING_CHANNEL_ID = os.getenv("SLACK_ONBOARDING_CHANNEL_ID")

# ==============================
# Google Sheets
# ==============================
GOOGLE_SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

# ==============================
# Email (SES)
# ==============================
SENDER_EMAIL = os.getenv("SENDER_EMAIL")