import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de .env

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")
HOSTED_ZONE_ID = os.getenv("HOSTED_ZONE_ID")
BUCKET_NAME = os.getenv("BUCKET_NAME")
LOCAL_BACKUP_DIR = os.getenv("LOCAL_BACKUP_DIR", "./route53-backups")