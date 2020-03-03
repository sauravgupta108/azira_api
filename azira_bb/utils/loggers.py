import logging
import os

from azira_api.settings import LOG_DIRECTORY, SUPER_LOG_FILE


def super_logger():
    logger = logging.getLogger("PARENT")

    log_handler = logging.FileHandler(SUPER_LOG_FILE)
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    log_handler.setFormatter(log_formatter)

    logger.addHandler(log_handler)
    return logger


def base_logger(logger_name, file_name):
    logger = logging.getLogger(logger_name)

    log_handler = logging.FileHandler(os.path.join(LOG_DIRECTORY, file_name))
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(log_formatter)

    logger.addHandler(log_handler)

    return logger


def comment_logger():
    return base_logger("comment", "comments.log")


def designation_logger():
    return base_logger("designation", "designation.log")


def issue_logger():
    return base_logger("issues", "issues.log")


def organization_logger():
    return base_logger("organizations", "organization.log")


def project_logger():
    return base_logger("projects", "projects.log")


def sprint_logger():
    return base_logger("sprints", "sprints.log")


def team_logger():
    return base_logger("teams", "teams.log")


def user_logger():
    return base_logger("users", "users.log")
