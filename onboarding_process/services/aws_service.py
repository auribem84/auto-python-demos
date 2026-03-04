import boto3
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION

def create_customer_bucket(customer_name):
    bucket_name = f"{customer_name.lower().replace(' ', '-')}-data"

    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION,
    )

    if AWS_REGION == "us-east-1":
        s3.create_bucket(Bucket=bucket_name)
    else:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                "LocationConstraint": AWS_REGION
            }
        )

    return bucket_name