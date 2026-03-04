from slack_sdk import WebClient
from config import SLACK_BOT_TOKEN, SLACK_ONBOARDING_CHANNEL_ID

def notify_onboarding_channel(customer_name, email, bucket_name):
    client = WebClient(token=SLACK_BOT_TOKEN)

    message = f"""
🚀 *New Customer Onboarded*

• *Customer ID:*
• *Name:* {customer_name}
• *Email:* {email}
• *S3 Bucket:* `{bucket_name}`

Everything is ready ✅
"""

    client.chat_postMessage(
        channel=SLACK_ONBOARDING_CHANNEL_ID,
        text=message
    )