import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

from src.config.app_settings import load_app_settings

_LOGGING_CONFIGURED = False

# -------------------------------------------------------------------------------------


def configure_logging():
    global _LOGGING_CONFIGURED

    if _LOGGING_CONFIGURED:
        return logging.getLogger()

    settings = load_app_settings()

    log_level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_name, logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    log_dir = Path(settings["log_dir"])
    log_dir.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        log_dir / "etl_tentativas_score.log",
        maxBytes=1_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    _LOGGING_CONFIGURED = True

    return root_logger


# -------------------------------------------------------------------------------------
