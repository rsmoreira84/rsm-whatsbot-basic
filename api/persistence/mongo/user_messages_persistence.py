import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class UserMessagesPersistence:

    def __init__(self, db_connection=None):
        self.db = db_connection
        self.user_messages_collection = self.db["user_messages"]

    def save_whatsapp_message_history(self, sender: str, message_text: str, timestamp: datetime, state: str) -> bool:
        logger.debug(f"Saving message history - sender {sender} - state {state} - message {message_text} - timestamp {datetime}")
        try:
            self.user_messages_collection.insert_one({
                "_id": str(uuid.uuid4()),
                "number": sender,
                "message": message_text,
                "state": state,
                "createdAt": timestamp
            })

        except Exception as e:
            logger.error(f"MongoDB Error: Failed to save message for {sender}. Exception: {e}")
            return False
