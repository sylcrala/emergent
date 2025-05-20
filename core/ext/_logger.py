import os
import json
from core.ext.config_loader import load_config  # or inline config if easier
import logging
from logging.handlers import RotatingFileHandler


#defining new log levels
USER_LEVEL = 25
SYSTEM_LEVEL = 35
MEMORY_LEVEL = 45
WARN_LEVEL = 60

logging.addLevelName(USER_LEVEL, "USER"),
logging.addLevelName(SYSTEM_LEVEL, "SYSTEM"),
logging.addLevelName(MEMORY_LEVEL, "MEMORY"),
logging.addLevelName(WARN_LEVEL, "WARNING")

#

#import config
config = load_config()
log_cfg = config.get("logging", {})
#

level_str = log_cfg.get("level", "INFO").upper()
custom_levels = {
    "USER": USER_LEVEL,
    "SYSTEM": SYSTEM_LEVEL,
    "MEMORY": MEMORY_LEVEL,
    "WARNING": WARN_LEVEL
    }

log_file = log_cfg.get('log_path', None)
log_to_file = log_cfg.get("log_to_file", True)

handlers = [logging.StreamHandler(), RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)]
if log_to_file and log_file:
    try:
        handlers.insert(0, logging.FileHandler(log_file))
    except Exception as e:
        print(f"[FATAL] LOGGING: failure while saving to file")


logging.basicConfig(
    level=USER_LEVEL or SYSTEM_LEVEL or MEMORY_LEVEL or WARN_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=handlers
)

logger = logging.getLogger("iris_logger")
