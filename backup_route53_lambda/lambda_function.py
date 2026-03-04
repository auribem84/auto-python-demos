import boto3
import json
import os
from datetime import datetime, timezone, timedelta

# -------------------------------
# CONFIGURACIÓN DESDE ENVIRONMENT VARIABLES
# -------------------------------
HOSTED_ZONE_ID = os.environ["HOSTED_ZONE_ID"]
BUCKET_NAME = os.environ["BUCKET_NAME"]
RETENTION_DAYS = int(os.environ.get("RETENTION_DAYS", 30))  # eliminar backups viejos

# Lambda solo puede escribir en /tmp
TMP_DIR = "/tmp/route53-backups"
os.makedirs(TMP_DIR, exist_ok=True)

def convert_to_bind(records, zone_name):
    """Convierte JSON de Route53 a formato tipo BIND"""
    lines = [f"$ORIGIN {zone_name}.", f"$TTL 300"]
    for r in records:
        name = r["Name"]
        rtype = r["Type"]
        ttl = r.get("TTL", 300)
        # Manejar múltiples valores
        if "ResourceRecords" in r:
            for rr in r["ResourceRecords"]:
                value = rr["Value"]
                lines.append(f"{name} {ttl} IN {rtype} {value}")
        elif "AliasTarget" in r:
            alias = r["AliasTarget"]["DNSName"]
            lines.append(f"{name} {ttl} IN {rtype} {alias}")
    return "\n".join(lines)

def lambda_handler(event, context):
    # Conexión AWS
    route53 = boto3.client("route53")
    s3 = boto3.client("s3")

    # Nombre de archivo con fecha
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    json_file = f"{TMP_DIR}/backup_{date_str}.json"
    zone_file = f"{TMP_DIR}/backup_{date_str}.zone"

    # -------------------------------
    # OBTENER REGISTROS DNS
    # -------------------------------
    try:
        paginator = route53.get_paginator("list_resource_record_sets")
        records = []

        for page in paginator.paginate(HostedZoneId=HOSTED_ZONE_ID):
            records.extend(page["ResourceRecordSets"])

        # Guardar JSON
        with open(json_file, "w") as f:
            json.dump(records, f, indent=2)

        # Generar archivo tipo BIND
        # Obtenemos el nombre del dominio desde la zona
        zone_info = route53.get_hosted_zone(Id=HOSTED_ZONE_ID)
        zone_name = zone_info["HostedZone"]["Name"]
        bind_content = convert_to_bind(records, zone_name)

        with open(zone_file, "w") as f:
            f.write(bind_content)

        print(f"Backups creados: {json_file}, {zone_file}")

    except Exception as e:
        print("Error obteniendo registros de Route53:", e)
        raise e

    # -------------------------------
    # SUBIR BACKUP A S3
    # -------------------------------
    try:
        for file_path in [json_file, zone_file]:
            s3.upload_file(file_path, BUCKET_NAME, os.path.basename(file_path))
            print(f"Subido a S3: {os.path.basename(file_path)}")

    except Exception as e:
        print("Error subiendo backups a S3:", e)
        raise e

    # -------------------------------
    # ELIMINAR BACKUPS ANTIGUOS
    # -------------------------------
    try:
        cutoff = datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        if "Contents" in response:
            for obj in response["Contents"]:
                if obj["LastModified"] < cutoff:
                    s3.delete_object(Bucket=BUCKET_NAME, Key=obj["Key"])
                    print(f"Eliminado backup antiguo: {obj['Key']}")

    except Exception as e:
        print("Error eliminando backups antiguos:", e)

    return {
        "statusCode": 200,
        "body": f"Backups completados: {os.path.basename(json_file)}, {os.path.basename(zone_file)}"
    }