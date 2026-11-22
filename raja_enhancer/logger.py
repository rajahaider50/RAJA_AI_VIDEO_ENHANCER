
import logging
from datetime import datetime
from .config import LOG_DIR, ensure_directories

def get_logger():
    ensure_directories()
    logger = logging.getLogger("raja_enhancer")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    log_file = LOG_DIR / f"session_{datetime.now():%Y%m%d}.log"
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger
