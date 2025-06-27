import logging
from pymongo import MongoClient
from .scripts.indexes import configure_user_messages_indexes, configure_users_indexes, configure_user_draft_indexes

logger = logging.getLogger(__name__)


def initialize_mongodb(app_config):
    """
    Initializes and returns a MongoDB client and database instance.
    Takes Flask app.config as an argument.
    """
    mongodb_uri = app_config.MONGODB_URI

    if not mongodb_uri:
        logger.error("MONGODB_URI is not set in application config.")
        return None, None

    try:
        mongo_client = MongoClient(mongodb_uri, uuidRepresentation='standard')
        db = mongo_client.get_database()  # Gets the database from the URI, or default if not specified
        # Optional: Ping the database to ensure connection
        mongo_client.admin.command('ping')
        logger.info(f"Successfully connected to MongoDB!")
        configure_user_messages_indexes(db)
        configure_users_indexes(db)
        configure_user_draft_indexes(db)
        return mongo_client, db
    except Exception as e:
        logger.error(f"Error connecting to MongoDB! {e}")
        return None, None
