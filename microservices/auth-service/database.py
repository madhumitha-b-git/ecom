import os
import boto3
import json
from config import settings
from logger import get_logger

logger = get_logger(__name__)

class LocalUserDB:
    def __init__(self, filename="db_users.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump({}, f)

    def _read(self):
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    def _write(self, data):
        try:
            with open(self.filename, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logger.error("LocalDB | Failed to write: %s", e)

    def put_item(self, Item):
        data = self._read()
        email = Item["email"]
        data[email] = Item
        self._write(data)
        logger.info(f"LocalDB | Saved user: {email}")

    def get_item(self, Key):
        data = self._read()
        email = Key["email"]
        item = data.get(email)
        if item:
            return {"Item": item}
        return {}

    def update_item(self, Key, UpdateExpression, ExpressionAttributeNames, ExpressionAttributeValues):
        data = self._read()
        email = Key["email"]
        if email not in data:
            return
        
        status_val = ExpressionAttributeValues.get(":s")
        if status_val:
            data[email]["status"] = status_val
        
        self._write(data)
        logger.info(f"LocalDB | Updated user status: {email} -> {status_val}")

    def scan(self):
        data = self._read()
        return {"Items": list(data.values())}


_db_client = None
_use_local = False

def get_db():
    global _db_client, _use_local
    if _db_client is not None:
        return _db_client

    if _use_local:
        _db_client = LocalUserDB()
        return _db_client

    try:
        if os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
            resource = boto3.resource("dynamodb", region_name=settings.AWS_REGION)
        else:
            session = boto3.Session(profile_name=settings.AWS_PROFILE)
            resource = session.resource("dynamodb", region_name=settings.AWS_REGION)
        
        table = resource.Table(settings.TABLE_NAME)
        table.table_status
        _db_client = table
        logger.info("DynamoDB | Connected to AWS table: %s", settings.TABLE_NAME)
    except Exception as e:
        logger.warning("DynamoDB | Connection failed: %s. Falling back to local file-based database.", e)
        _use_local = True
        _db_client = LocalUserDB()
    
    return _db_client
