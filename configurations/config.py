import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key-for-local')
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')  # Default to production
    DEBUG = False
    TESTING = False

    # Server Settings
    PORT = int(os.getenv('PORT', 3000))
    HOST = os.getenv('HOST', '0.0.0.0')

    # Database connections
    MONGODB_URI = os.getenv('MONGODB_URI')
    REDIS_URL = os.getenv('REDISCLOUD_URL')

    if not MONGODB_URI:
        raise ValueError("No MONGODB_URI set for Flask application. Please set it in .env or Heroku config vars.")
    if not REDIS_URL:
        raise ValueError("No REDIS_URL set for Flask application. Please set it in .env or Heroku config vars.")

    # Logging configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()


class DevelopmentConfig(Config):
    """Development specific configuration."""
    DEBUG = True
    FLASK_ENV = 'development'
    # # For local development with docker-compose, these will point to localhost
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/whatsbot-bakery')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')


class ProductionConfig(Config):
    """Production specific configuration (for Heroku)."""
    FLASK_ENV = 'production'
    # # Heroku will provide MONGODB_URI and REDIS_URL via add-ons as environment variables.
    # # The default value (None) will be overridden by Heroku's injected env vars.
    # MONGODB_URI = os.getenv('MONGODB_URI')
    # REDIS_URL = os.getenv('REDIS_URL')
    # # More production-specific settings can go here (e.g., logging)


def get_config():
    """
    Returns the appropriate configuration class based on FLASK_ENV environment variable.
    Defaults to ProductionConfig if FLASK_ENV is not set or recognized.
    """
    env = os.getenv('FLASK_ENV', 'production')
    if env == 'development':
        return DevelopmentConfig
    else:
        return ProductionConfig
