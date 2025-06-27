import redis
import logging

logger = logging.getLogger(__name__)


def initialize_redis(app_config):
    """
    Initializes and returns a Redis client instance.
    Takes Flask app.config as an argument.
    """
    redis_url = app_config.REDIS_URL

    if not redis_url:
        logger.error("REDIS_URL is not set in application config.")
        return None

    try:
        redis_client = redis.from_url(redis_url)
        # Optional: Ping Redis to ensure connection
        redis_client.ping()
        logger.info(f"Successfully connected to Redis!")
        return redis_client
    except Exception as e:
        logger.error(f"Error connecting to Redis! {e}")
        return None
