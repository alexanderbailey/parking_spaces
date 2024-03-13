import coloredlogs
import logging

logger = logging.getLogger(__name__)


def use_root_handler(_logger):
    """
    Setting up the base to build the internal logger from

    Args:
        _logger:
    """
    _logger.handlers = []
    _logger.addHandler(logging.root.handlers[0])


def setup_logging():
    """
    Set up the logging system
    """
    coloredlogs.install(
        level="DEBUG", fmt="%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s"
    )
    logging.root.setLevel("INFO")
    # --
    _logger = logging.getLogger("uvicorn.access")
    use_root_handler(_logger)

    # sqlalchemy logger requires special treatment...
    # if config.log_sql_alchemy:
    logger.info("Enabling sqlalchemy SQL logging")
    # logging.getLogger("sqlalchemy.engine.Engine").setLevel("INFO")


def get_logger() -> logging.Logger:
    """
    Returns:
        (logging.Logger): The current logger
    """
    return logging.getLogger("uvicorn.access")
