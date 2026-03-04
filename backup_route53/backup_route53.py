import boto3
import json
import os
from datetime import datetime
from app.config import (
    AWS_ACCESS_KEY,
    AWS_SECRET_KEY,
    AWS_REGION,
    HOSTED_ZONE_ID,
    BUCKET_NAME,
    LOCAL_BACKUP_DIR,
)

# Crear directorio local si no existe
os.makedirs(LOCAL_BACKUP_DIR, exist_ok=True)

# Nombre de archivo con fecha
date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_file = f"{LOCAL_BACKUP_DIR}/backup_{date_str}.json"

# -------------------------------
# CONEXIÓN A AWS
# -------------------------------
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)

route53 = session.client("route53")
s3 = session.client("s3")

# -------------------------------
# OBTENER REGISTROS DNS
# -------------------------------
try:
    paginator = route53.get_paginator("list_resource_record_sets")
    records = []

    for page in paginator.paginate(HostedZoneId=HOSTED_ZONE_ID):
        records.extend(page["ResourceRecordSets"])

    # Guardar backup local
    with open(backup_file, "w") as f:
        json.dump(records, f, indent=2)

    print(f"Backup local creado: {backup_file}")

except Exception as e:
    print("Error obteniendo registros de Route 53:", e)
    exit(1)

# -------------------------------
# SUBIR BACKUP A S3
# -------------------------------
try:
    s3.upload_file(backup_file, BUCKET_NAME, os.path.basename(backup_file))
    print(f"Backup subido a S3: s3://{BUCKET_NAME}/{os.path.basename(backup_file)}")
except Exception as e:
    print("Error subiendo backup a S3:", e)