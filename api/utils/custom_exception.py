class GeneralAppError(Exception):
    """Base exception for My Application."""
    pass


class DatabaseError(GeneralAppError):
    """Exception related to database operations."""

    def __init__(self, message="Database error", db_code=None):
        self.db_code = db_code
        super().__init__(f"{message} (DB Code: {db_code})" if db_code else message)


class RedisError(GeneralAppError):
    """Exception related to redis operations."""

    def __init__(self, message="Redis error", redis_code=None):
        self.redis_code = redis_code
        super().__init__(f"{message} (Redis Code: {redis_code})" if redis_code else message)
