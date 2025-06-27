import logging
from pymongo import ASCENDING

logger = logging.getLogger(__name__)


def configure_user_messages_indexes(db):
    logger.info("Configuring indexes")
    collection_name = "user_messages"

    user_messages_collection = db[collection_name]

    ttl_index_name = "createdAt_ttl_index"
    ttl_index_key = "createdAt"
    ttl_expiration_seconds = 3600  # 1h

    try:
        user_messages_collection.create_index(
            ttl_index_key,
            name=ttl_index_name,
            expireAfterSeconds=ttl_expiration_seconds,
            background=True  # Recommended for non-blocking creation in production
        )
        logger.info(f"Collection {collection_name}: Index '{ttl_index_name}' created or already exists.")
        logger.info(f"{collection_name} collection: indexes configured successfully.")
    except Exception as e:
        logger.error(f"{collection_name} collection: Error creating index '{ttl_index_name}': {e}")


def configure_users_indexes(db):
    logger.info("Configuring indexes")
    collection_name = "users"
    collection = db[collection_name]

    index_name = "number_uk_index"

    try:
        collection.create_index(
            [("number", ASCENDING)],
            name=index_name,
            unique=True,
            background=True  # Recommended for non-blocking creation in production
        )
        logger.info(f"Collection {collection_name}: Index '{index_name}' created or already exists.")
        logger.info(f"{collection_name} collection: indexes configured successfully.")
    except Exception as e:
        logger.error(f"Collection {collection_name}: Error creating index '{index_name}': {e}")


def configure_user_draft_indexes(db):
    logger.info("Configuring indexes")
    collection_name = "user_draft"
    collection = db[collection_name]

    index_name = "number_draft_type_uk_index"

    try:
        collection.create_index(
            [("number", ASCENDING), ("draft_type", ASCENDING)],
            name=index_name,
            unique=True,
            background=True  # Recommended for non-blocking creation in production
        )
        logger.info(f"Collection {collection_name}: Index '{index_name}' created or already exists.")
        logger.info(f"{collection_name} collection: indexes configured successfully.")
    except Exception as e:
        logger.error(f"Collection {collection_name}: Error creating index '{index_name}': {e}")