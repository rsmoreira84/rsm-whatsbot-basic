import os
import sys
import platform
import logging
from flask import Flask
from api.routes import routes
from configurations.config import get_config
from configurations.mongo.db_config import initialize_mongodb
from configurations.redis.redis_config import initialize_redis
from configurations.logging import configure_logging

app = Flask(__name__)
config = get_config()

configure_logging(config)
logger = logging.getLogger(__name__)

logger.info("----------------------------------------------------")
logger.info(f"Starting Python service: {__file__}")
logger.info(f"Python Version: {sys.version}")
logger.info(f"Python Executable: {sys.executable}")
logger.info(f"Platform: {platform.platform()}")
logger.info("----------------------------------------------------")

app.config.from_object(config)
app.mongo_client, app.db = initialize_mongodb(config)
app.redis_client = initialize_redis(config)
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(
        host=os.getenv('HOST', config.HOST),
        port=os.getenv('PORT', config.PORT),
        debug=config.DEBUG
    )
