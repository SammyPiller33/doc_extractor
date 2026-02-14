import logging
from logging.handlers import RotatingFileHandler

def get_logger(name: str) -> logging.Logger:
    """
    Create and configure logger with standard output and rotating log file.

    Args:
        name (str): Name of the logger

    Returns:
        logging.Logger: Logger with handlers console (INFO+) and file (DEBUG+)

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Application démarrée")
    """
    # Get (or create) a logger with a given name
    logger = logging.getLogger(name)

    # Define minimum logging level as DEBUG: all lower levels are ignored.
    logger.setLevel(logging.DEBUG)

    # If handlers exists, return logger.
    if logger.handlers:
        return logger

    # ===== Handler console =====
    # Handler for sending to the standard output (terminal/console).
    console_handler = logging.StreamHandler()
    # Define minimum logging level for console handler as INFO: DEBUG level ignored.
    console_handler.setLevel(logging.INFO)

    # ===== Rotating file handler =====
    # RotatingFileHandler creates a new log file when it gets a certain size.
    file_handler = RotatingFileHandler(
        filename="./app.log",       # Name of the log file
        maxBytes=2_000_000,         # Max size before rotation (~2 Mo)
        backupCount=5,              # Number of kept log files
        encoding="utf-8",           # File encoding: defines how characters are converted into bytes.
    )
    # Define minimum logging level for file handler as DEBUG: all logs are saved in the file.
    file_handler.setLevel(logging.DEBUG)

    # ===== Log formating =====
    # Define the format of each log record.
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    # Apply format to handlers
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Attach handlers to the logger.
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Return logger to be used in the application.
    return logger
