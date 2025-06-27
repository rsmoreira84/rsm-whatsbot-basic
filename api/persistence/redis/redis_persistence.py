import json
import logging
from typing import Union

logger = logging.getLogger(__name__)


class RedisPersistence:

    def __init__(self, redis_client):
        self.redis_client = redis_client

    def set_state(self, key: str, value: dict, ex_seconds: int = None) -> bool:
        try:
            # Redis stores strings, so we serialize the dictionary to a JSON string
            serialized_value = json.dumps(value)
            self.redis_client.set(key, serialized_value, ex=ex_seconds)
            logger.debug(f"Redis: Set key '{key}' with value '{value}'.")
            return True
        except Exception as e:
            logger.error(f"Redis Error: Failed to set key '{key}'. Exception: {e}")
            return False

    def get_state(self, key: str) -> Union[dict, None]:
        try:
            retrieved_value = self.redis_client.get(key)
            if retrieved_value:
                # Redis returns bytes, so decode to string then deserialize from JSON
                deserialized_value = json.loads(retrieved_value.decode('utf-8'))
                logger.debug(f"Redis: Got key '{key}' with value '{deserialized_value}'.")
                return deserialized_value
            logger.debug(f"Redis: Key '{key}' not found.")
            return None
        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"Redis Error: Failed to get or deserialize key '{key}'. Exception: {e}")
            return None

    def delete_state(self, key: str) -> bool:
        try:
            deleted_count = self.redis_client.delete(key)
            if deleted_count > 0:
                logger.debug(f"Redis: Deleted key '{key}'.")
                return True
            logger.debug(f"Redis: Key '{key}' not found for deletion.")
            return False
        except Exception as e:
            logger.error(f"Redis Error: Failed to delete key '{key}'. Exception: {e}")
            return False
