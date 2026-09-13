import logging
from typing import Optional


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


def set_debug(enabled: bool = False) -> None:
    level = logging.DEBUG if enabled else logging.INFO
    logging.getLogger().setLevel(level)
