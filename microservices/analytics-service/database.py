import os
import json
import time
import boto3
from config import settings
from logger import get_logger

logger = get_logger(__name__)

def get_s3_client():
    if os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        return boto3.client("s3", region_name=settings.AWS_REGION)
    else:
        session = boto3.Session(profile_name=settings.AWS_PROFILE)
        return session.client("s3", region_name=settings.AWS_REGION)

def write_raw_event(event_type: str, data: dict):
    """Write an event to the S3 Raw Bucket."""
    if not settings.S3_RAW_BUCKET:
        logger.warning("DataLake | S3_RAW_BUCKET not configured. Skipping write.")
        return

    filename = f"{event_type}_{int(time.time() * 1000)}.json"
    try:
        event_wrapper = {
            "event_type": event_type,
            "timestamp": time.time(),
            "data": data
        }
        s3 = get_s3_client()
        s3.put_object(
            Bucket=settings.S3_RAW_BUCKET,
            Key=filename,
            Body=json.dumps(event_wrapper, indent=4),
            ContentType="application/json"
        )
        logger.info(f"DataLake | Raw event written to S3: {filename}")
    except Exception as e:
        logger.error(f"DataLake | Failed to write raw event to S3: {e}")

def get_raw_events() -> list[dict]:
    """Read all raw events from S3 Raw Bucket."""
    events = []
    if not settings.S3_RAW_BUCKET:
        return events

    try:
        s3 = get_s3_client()
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=settings.S3_RAW_BUCKET)
        
        for page in pages:
            if "Contents" in page:
                for obj in page["Contents"]:
                    key = obj["Key"]
                    if key.endswith(".json"):
                        try:
                            response = s3.get_object(Bucket=settings.S3_RAW_BUCKET, Key=key)
                            events.append(json.loads(response['Body'].read().decode('utf-8')))
                        except Exception as e:
                            logger.error(f"DataLake | Failed to read raw event {key}: {e}")
    except Exception as e:
        logger.error(f"DataLake | Failed to list raw events in S3: {e}")
    return events

def write_stage_data(report_name: str, data: dict):
    """Write processed ETL aggregations to S3 Stage Bucket."""
    if not settings.S3_STAGE_BUCKET:
        logger.warning("DataLake | S3_STAGE_BUCKET not configured. Skipping write.")
        return

    filename = f"{report_name}.json"
    try:
        s3 = get_s3_client()
        s3.put_object(
            Bucket=settings.S3_STAGE_BUCKET,
            Key=filename,
            Body=json.dumps(data, indent=4),
            ContentType="application/json"
        )
        logger.info(f"DataLake | Stage report written to S3: {filename}")
    except Exception as e:
        logger.error(f"DataLake | Failed to write stage report to S3: {e}")

def get_stage_data(report_name: str) -> dict:
    """Read processed data from S3 Stage Bucket."""
    if not settings.S3_STAGE_BUCKET:
        return {}

    filename = f"{report_name}.json"
    try:
        s3 = get_s3_client()
        response = s3.get_object(Bucket=settings.S3_STAGE_BUCKET, Key=filename)
        return json.loads(response['Body'].read().decode('utf-8'))
    except s3.exceptions.NoSuchKey:
        return {}
    except Exception as e:
        logger.error(f"DataLake | Failed to read stage report {filename} from S3: {e}")
        return {}
