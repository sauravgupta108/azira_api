import logging


def log_message(log_msg, log_type="info"):
    logger = logging.getLogger(__name__)

    if log_type.lower() == "info":
        logger.info(log_msg)
    elif log_type.lower() == "debug":
        logger.debug(log_msg)
    elif log_type.lower() == "warning":
        logger.warning(log_msg)
    elif log_type.lower() in ["error", "exception"]:
        logger.error(log_msg)
    else:
        logger.info(log_msg)
