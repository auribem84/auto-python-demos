#from services.db_service import create_customer
from services.aws_service import create_customer_bucket
from services.slack_service import notify_onboarding_channel
#from services.spreadsheet_service import add_customer_to_sheet
from services.email_service import send_welcome_email

def onboard_customer(customer_name, email):
    print("Creating DB record...")
    #customer_id = create_customer(customer_name, email)

    print("Creating S3 bucket...")
    bucket_name = create_customer_bucket(customer_name)

    print("Adding to spreadsheet...")
    #add_customer_to_sheet(customer_id, customer_name, email, bucket_name)

    print("Sending Slack notification...")
    notify_onboarding_channel(customer_name, email, bucket_name)

    print("Sending welcome email...")
    send_welcome_email(email, customer_name)

    print("Onboarding complete ✅")

if __name__ == "__main__":
    onboard_customer("HHCenterCC", "auribem84@gmail.com")