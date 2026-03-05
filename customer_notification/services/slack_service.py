from slack_sdk import WebClient
from config import SLACK_BOT_TOKEN, SLACK_ALERT_CHANNEL_ID


def notify_internal_team(customer_name, amount):
    client = WebClient(token=SLACK_BOT_TOKEN)

    message = f"""
⚠️ Overdue Payment Reminder Sent

Customer: {customer_name}
Amount: ${amount}

Notification email delivered.
"""

    client.chat_postMessage(
        channel=SLACK_ALERT_CHANNEL_ID,
        text=message
    )