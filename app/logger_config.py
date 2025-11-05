import logging
import os
from datetime import datetime

def setup_logger(logger_name, log_prefix):
    """
    Sets up a logger that creates log files in a structured directory format.
    e.g., logs/Nov25/telegram_05.11.2025.log
    """
    # Create base logs directory
    base_log_dir = 'logs'
    if not os.path.exists(base_log_dir):
        os.makedirs(base_log_dir)

    # Create subdirectory for the current month and year (e.g., Nov25)
    month_year_dir = os.path.join(base_log_dir, datetime.now().strftime('%b%y'))
    if not os.path.exists(month_year_dir):
        os.makedirs(month_year_dir)

    # Define log file name and path
    log_filename = f"{log_prefix}_{datetime.now().strftime('%d.%m.%Y')}.log"
    log_filepath = os.path.join(month_year_dir, log_filename)

    # Get logger and set level
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Avoid adding duplicate handlers
    if not logger.handlers:
        # Create file handler
        file_handler = logging.FileHandler(log_filepath)
        file_handler.setLevel(logging.INFO)

        # Create log formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)

        # Add handler to the logger
        logger.addHandler(file_handler)

    return logger
