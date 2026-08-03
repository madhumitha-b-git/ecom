import os
import boto3
from config import settings

_table = None


def get_table():
    global _table
    if _table is None:
        if os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
            resource = boto3.resource("dynamodb", region_name=settings.AWS_REGION)
        else:
            session = boto3.Session(profile_name=settings.AWS_PROFILE)
            resource = session.resource("dynamodb", region_name=settings.AWS_REGION)
        _table = resource.Table(settings.TABLE_NAME)
    return _table