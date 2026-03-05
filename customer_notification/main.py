import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.notification_service import process_notifications


if __name__ == "__main__":
    print("Starting customer notification process...")
    process_notifications()
    print("Process finished ✅")