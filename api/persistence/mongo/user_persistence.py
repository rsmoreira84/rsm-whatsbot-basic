import uuid
import logging
from pymongo.results import UpdateResult, InsertOneResult

logger = logging.getLogger(__name__)


class UserPersistence:

    def __init__(self, db_connection):
        self.db = db_connection
        self.users_collection = self.db["users"]

    def find_user(self, sender: str):
        logger.debug(f"Finding user - sender {sender}")
        try:
            user = self.users_collection.find_one({"number": sender})
            if user:
                logger.debug(f"MongoDB: Found user {sender}.")
            else:
                logger.debug(f"MongoDB: User {sender} not found.")
            return user
        except Exception as e:
            logger.error(f"MongoDB Error: Failed to find user {sender}. Exception: {e}")
            return None

    def delete_user(self, sender: str):
        logger.debug(f"Deleting user - sender {sender}")
        try:
            return self.users_collection.delete_one({"number": sender})

        except Exception as e:
            logger.error(f"MongoDB Error: Failed to delete user {sender}. Exception: {e}")
            return 0

    def update_user_property(self, sender: str, value: str, prop: str):
        logger.debug(f"Updating user prop - sender {sender} - prop {prop} - value {value}")
        try:
            result: UpdateResult = self.users_collection.update_one(
                {"number": sender},
                {"$set": {prop: value}}
            )

            if result.matched_count == 0:
                insert_result: InsertOneResult = self.users_collection.insert_one(
                    {"_id": str(uuid.uuid4()), "number": sender, prop: value}
                )
                logger.debug(f"Inserted new user with _id: {insert_result.inserted_id}")
                return insert_result
            else:
                logger.debug(f"Updated user with number: {sender}")
                return result

        except Exception as e:
            logger.error(f"MongoDB Error: Failed to update user name - {sender}. Exception: {e}")
            return None
