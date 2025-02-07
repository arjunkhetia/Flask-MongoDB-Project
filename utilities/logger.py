import os
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

# Create logs directory if not exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configure logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s"
LOG_FILE = "logs/app.log"
MAX_LOG_SIZE = 1024 * 1024  # 1 MB
BACKUP_COUNT = 10 # Keep last 10 log files
TIME_INTERVAL = 1 # 1 day
TIME_INTERVAL_UNIT = "D" # D for day, S for second, M for minute, H for hour

# Basic logger
logging.basicConfig(
    level = logging.NOTSET,
    format = LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)

# Create a time based rotating file handler
# file_handler = TimedRotatingFileHandler(LOG_FILE, when=TIME_INTERVAL_UNIT, interval=TIME_INTERVAL, backupCount=BACKUP_COUNT)
# file_handler.setLevel(logging.NOTSET)  # Set log level for file handler
# file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
# logging.getLogger().addHandler(file_handler)  # Add file handler to root logger
# logging.getLogger().setLevel(logging.NOTSET)  # Set log level for root logger
# logging.getLogger().addHandler(logging.StreamHandler())  # Add console handler to root logger


# Create a file size based rotating file handler
# file_handler = RotatingFileHandler(LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
# file_handler.setLevel(logging.NOTSET)  # Set log level for file handler
# file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
# logging.getLogger().addHandler(file_handler)  # Add file handler to root logger
# logging.getLogger().setLevel(logging.NOTSET)  # Set log level for root logger
# logging.getLogger().addHandler(logging.StreamHandler())  # Add console handler to root logger


# Get logger instance
logger = logging.getLogger("flask_app")