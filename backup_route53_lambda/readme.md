📦 Backup Automático de Route 53 con Lambda

Este proyecto implementa una función AWS Lambda que realiza un backup automático de tus zonas DNS en Route 53, generando:

Archivo JSON con todos los registros (.json)

Archivo tipo BIND/zone (.zone) para restauración rápida

Los backups se suben a S3 y se eliminan automáticamente los antiguos según la política de retención.

🔹 Funcionamiento del Lambda
+--------------------+
|  EventBridge Cron  |  → Dispara Lambda según programación
+--------------------+
           |
           v
+--------------------+
|    AWS Lambda      |  → Código Python ejecuta:
| - Obtiene registros|
| - Crea JSON & zone |
| - Guarda temporal  |
+--------------------+
           |
           v
+--------------------+
|     S3 Bucket      |  → Guarda backups
| - backup_YYYY-MM-DD.json
| - backup_YYYY-MM-DD.zone
+--------------------+
           |
           v
+--------------------+
| Cleanup automático |  → Elimina backups > RETENTION_DAYS
+--------------------+
🔹 Variables de entorno necesarias
Variable	Descripción
HOSTED_ZONE_ID	ID de la zona Route 53 que quieres respaldar
BUCKET_NAME	Nombre del bucket S3 donde se guardarán los backups
RETENTION_DAYS	Cantidad de días para mantener backups antes de eliminar (default 30)
AWS_ACCESS_KEY	Access Key de tu usuario con permisos Route 53 y S3 (solo para pruebas locales)
AWS_SECRET_KEY	Secret Key del usuario AWS
AWS_REGION	Región AWS para conexión con S3 y Route 53

Nota: Lambda solo permite escribir en /tmp, por eso los archivos se generan ahí antes de subirlos a S3.
Para pruebas locales, se pueden usar .env y config.py.

🔹 Ejecución local (pruebas antes de desplegar Lambda)

Instalar dependencias:

pip install boto3 python-dotenv

Crear archivo .env en la raíz:

AWS_ACCESS_KEY=YOUR_ACCESS_KEY
AWS_SECRET_KEY=YOUR_SECRET_KEY
AWS_REGION=us-east-1
HOSTED_ZONE_ID=Z123456ABCDEF
BUCKET_NAME=my-route53-backups
LOCAL_BACKUP_DIR=./route53-backups
RETENTION_DAYS=30

Crear archivo config.py para leer variables:

import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")
HOSTED_ZONE_ID = os.getenv("HOSTED_ZONE_ID")
BUCKET_NAME = os.getenv("BUCKET_NAME")
LOCAL_BACKUP_DIR = os.getenv("LOCAL_BACKUP_DIR", "./route53-backups")
RETENTION_DAYS = int(os.getenv("RETENTION_DAYS", 30))

Ejecutar script de backup local:

python backup_route53_local.py

backup_route53_local.py puede ser la misma lógica del Lambda, pero usando config.py y escribiendo en LOCAL_BACKUP_DIR en tu máquina local en lugar de /tmp.

Verifica:

JSON y archivo .zone se generan en ./route53-backups/.

Puedes subirlos manualmente a S3 si quieres probar la parte de upload.

🔹 Deploy del Lambda

Crear función Lambda con runtime Python 3.11.

Asignar un IAM Role con permisos mínimos:

route53:ListResourceRecordSets

s3:PutObject

s3:DeleteObject

Configurar las variables de entorno indicadas arriba.

Subir lambda_function.py (zip si tienes dependencias).

Crear regla EventBridge para ejecución programada (ej: diario a las 2 AM UTC):

cron(0 2 * * ? *)
🔹 Estructura de archivos del proyecto
backup_route53_lambda/
│
├── lambda_function.py       # Código Lambda principal
├── backup_route53_local.py  # Script local para pruebas
├── config.py                # Configuración local con variables de entorno
├── .env                     # Variables para pruebas locales
├── README.md               # Documentación
└── requirements.txt        # Dependencias opcionales (python-dotenv)
🔹 Beneficios

Backup seguro y automatizado de Route 53

Archivos JSON y zone para restauración rápida

Limpieza automática de backups antiguos

Escalable y configurable con variables de entorno

Prueba local antes de deploy