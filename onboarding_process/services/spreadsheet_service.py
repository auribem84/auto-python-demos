import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from config import GOOGLE_SERVICE_ACCOUNT_FILE, GOOGLE_SHEET_ID

def add_customer_to_sheet(customer_id, name, email, bucket_name):
    credentials = service_account.Credentials.from_service_account_file(
        GOOGLE_SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    service = build("sheets", "v4", credentials=credentials)

    values = [[customer_id, name, email, bucket_name]]

    body = {"values": values}

    service.spreadsheets().values().append(
        spreadsheetId=GOOGLE_SHEET_ID,
        range="Sheet1!A:D",
        valueInputOption="RAW",
        body=body
    ).execute()