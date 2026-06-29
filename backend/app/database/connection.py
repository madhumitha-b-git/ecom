"""Single MongoDB client instance (singleton)."""

from pymongo import MongoClient
from pymongo.database import Database

from app.config import settings
from app.logger import get_logger

logger = get_logger(__name__)

_client: MongoClient | None = None


def get_client() -> MongoClient:
    """Return the singleton MongoClient, creating it on first call."""
    global _client
    if _client is None:
        logger.info("Connecting to MongoDB...")
        _client = MongoClient(settings.MONGODB_URI)
        logger.info("MongoDB connection established.")
    return _client


def get_database() -> Database:
    """Return the application database."""
    return get_client()[settings.DATABASE_NAME]
