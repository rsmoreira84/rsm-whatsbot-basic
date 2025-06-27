import uuid
import logging
from api.static.properties import *

logger = logging.getLogger(__name__)


class UserDraftPersistence:

    def __init__(self, db_connection):
        self.db = db_connection
        self.user_draft = self.db["user_draft"]

    def save_draft_data(self, draft_type: str, sender: str, message_text: str) -> bool:
        logger.debug(f"Saving user draft - sender {sender} - draft type {draft_type} - message {message_text}")
        try:
            self.user_draft.insert_one({
                "_id": str(uuid.uuid4()),
                "draft_type": draft_type,
                "number": sender,
                "value": message_text
            })
        except Exception as e:
            logger.error(f"MongoDB Error user_draft collection: Failed to save message for {sender}. Exception: {e}")
            return False

    def find_draft_data(self, draft_type: str, sender: str):
        logger.debug(f"Getting user draft - sender {sender} - draft type {draft_type}")
        try:
            draft = self.user_draft.find_one({"number": sender, "draft_type": draft_type})
            if draft:
                logger.debug(f"MongoDB: Found draft {draft_type} - {sender}.")
            else:
                logger.debug(f"MongoDB: draft {draft_type} - {sender} not found.")
            return draft
        except Exception as e:
            logger.error(f"MongoDB Error: Failed to find draft {draft_type} - {sender}. Exception: {e}")
            return None

    def delete_draft(self, sender: str, draft_type: str):
        logger.debug(f"Deleting user draft - sender {sender} - draft type {draft_type}")
        try:
            return self.user_draft.delete_one({"number": sender, "draft_type": draft_type})

        except Exception as e:
            logger.error(f"MongoDB Error: Failed to delete user {sender}. Exception: {e}")
            return 0

    def delete_all_drafts(self, sender: str):
        logger.debug(f"Deleting all user drafts - sender {sender}")
        try:
            return self.user_draft.delete_many({
                "number": sender,
                "draft_type": {
                    "$in": [
                        NAME,
                        EMAIL
                    ]
                }
            })

        except Exception as e:
            logger.error(f"MongoDB Error: Failed to delete user {sender}. Exception: {e}")
            return 0
