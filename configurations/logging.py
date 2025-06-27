import logging
import sys


def configure_logging(app_config):
    """
        Configures the root logger for the entire application.
        This function should be called once at the start of the program.
        """
    # 1. Get the desired log level from an environment variable, defaulting to 'INFO'.
    log_level_str = app_config.LOG_LEVEL

    # 2. Map the string to a logging level constant.
    numeric_level = getattr(logging, log_level_str, logging.INFO)

    # 3. Handle invalid log levels gracefully.
    if not isinstance(numeric_level, int):
        print(f"WARNING: Invalid log level '{log_level_str}' specified. Defaulting to 'INFO'.", file=sys.stderr)
        numeric_level = logging.INFO

    # 4. Configure the root logger.
    #    Once configured, all loggers created in other modules will inherit this configuration.
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        stream=sys.stdout
    )

    # 5. Get a logger instance for this module and log the configuration.
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured with level: {logging.getLevelName(numeric_level)}")
