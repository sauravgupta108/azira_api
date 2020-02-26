import logging
import re


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


def is_valid_phone_number(phone_number):
    if type(phone_number) != str:
        return False

    if len(phone_number) != 10:
        return False

    if not phone_number.isdecimal():
        return False

    return True


def is_valid_email_address(email_address):
    if type(email_address) != str:
        return False

    email_regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    return re.search(email_regex, email_address)
